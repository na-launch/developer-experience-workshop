from confluent_kafka import Producer, Consumer

# Produce
p = Producer({"bootstrap.servers": "localhost:9092"})
p.produce("test-topic", value="Hello ZooKeeper world!")
p.flush()

# Consume
c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "mygroup",
    "auto.offset.reset": "earliest"
})
c.subscribe(["test-topic"])
msg = c.poll(timeout=5)
if msg and not msg.error():
    print("Got:", msg.value().decode())
c.close()