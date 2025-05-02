import os
import asyncio
import time
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from aiokafka import AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

app = FastAPI(title="Real-Time Kafka Consumer")

# Mount the public folder at /static to serve CSS, images, etc.
app.mount("/static", StaticFiles(directory="public"), name="static")

# Get the Kafka bootstrap servers without a default;
# if not provided, we will disable the HTML page and consumer.
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_AVAILABLE = bool(KAFKA_BOOTSTRAP_SERVERS)
if not KAFKA_AVAILABLE:
    print("WARNING: KAFKA_BOOTSTRAP_SERVERS env var is not set. Disabling HTML and consumer startup.")

# Define the default topic and assign it as the current topic.
DEFAULT_TOPIC = "default-topic"
current_topic = DEFAULT_TOPIC
consumer_task = None

# List to hold active WebSocket connections
active_connections: List[WebSocket] = []

# Function to run the Kafka consumer on a given topic.
async def consume_kafka_messages(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=f"rewind-{int(time.time())}",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    print(f"Kafka consumer started, subscribed to topic='{topic}'")
    try:
        async for msg in consumer:
            message_str = msg.value.decode("utf-8")
            disconnected = []
            for conn in active_connections:
                try:
                    await conn.send_text(message_str)
                except Exception as e:
                    print(f"Failed to send message: {e}")
                    disconnected.append(conn)
            for d in disconnected:
                if d in active_connections:
                    active_connections.remove(d)
    finally:
        await consumer.stop()
        print("Kafka consumer stopped.")

# Data model for the topic change request.
class TopicChange(BaseModel):
    topic: str

# Endpoint to change the Kafka topic.
@app.post("/change_topic")
async def change_topic(topic_change: TopicChange):
    global current_topic, consumer_task
    new_topic = topic_change.topic.strip()
    if not new_topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    if new_topic == current_topic:
        return {"message": "Topic unchanged"}
    # Cancel the current consumer task if it exists.
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            print("Previous consumer task cancelled")
    current_topic = new_topic
    if KAFKA_AVAILABLE:
        consumer_task = asyncio.create_task(consume_kafka_messages(current_topic))
    return {"message": f"Topic changed to {new_topic}"}

# Endpoint to list all available topics, ensure the default topic exists,
# and filter out internal topics (like __consumer_offsets).
@app.get("/topics")
async def get_topics():
    if not KAFKA_AVAILABLE:
        raise HTTPException(status_code=503, detail="Kafka not configured.")
    admin_client = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await admin_client.start()
    try:
        topics = await admin_client.list_topics()
        topics_set = set(topics)

        # Create the default topic if it doesn't already exist.
        if DEFAULT_TOPIC not in topics_set:
            new_topic = NewTopic(DEFAULT_TOPIC, num_partitions=1, replication_factor=1)
            try:
                await admin_client.create_topics([new_topic])
                topics_set.add(DEFAULT_TOPIC)
                print(f"Default topic '{DEFAULT_TOPIC}' created.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to create default topic: {e}")

        # Filter out internal topics (those starting with '__').
        filtered_topics = [t for t in topics_set if not t.startswith("__")]

        # Ensure the default topic is the first in the list.
        if DEFAULT_TOPIC in filtered_topics:
            filtered_topics.remove(DEFAULT_TOPIC)
            filtered_topics.insert(0, DEFAULT_TOPIC)

        return {"topics": filtered_topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get topics: {e}")
    finally:
        await admin_client.close()

# Serve index.html at the root.
@app.get("/")
async def read_index():
    if not KAFKA_AVAILABLE:
        return HTMLResponse(
            "<h1>Error: KAFKA_BOOTSTRAP_SERVERS env var is not set.</h1>"
            "<p>Please configure this environment variable to enable the application.</p>",
            status_code=503
        )
    from pathlib import Path
    index_file = Path("public") / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)
    return HTMLResponse(index_file.read_text(encoding="utf-8"))

# WebSocket endpoint for real-time messages.
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    if not KAFKA_AVAILABLE:
        await websocket.close()
        return
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keeping connection open—no processing of client messages.
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# On startup, launch the Kafka consumer for the default topic if Kafka is configured.
@app.on_event("startup")
async def startup_event():
    global consumer_task
    if KAFKA_AVAILABLE:
        consumer_task = asyncio.create_task(consume_kafka_messages(current_topic))
        print("Startup event: Kafka consumer task created.")
    else:
        print("Startup event: Kafka is not configured; HTML and consumer are disabled.")
