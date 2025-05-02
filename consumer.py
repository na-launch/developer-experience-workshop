import os
import uuid
import argparse
import asyncio
import logging
import colorlog
from aiokafka import AIOKafkaConsumer

# ANSI styles for terminal colors
STYLES = {
    "blue": "\033[1;34m",
    "yellow": "\033[1;33m",
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "magenta": "\033[1;35m",
    "cyan": "\033[1;36m",
    "reset": "\033[0m"
}

# Emoji + color by topic
TOPIC_META = {
    "alerts":       {"emoji": "🚨", "style": STYLES["red"]},
    "health":       {"emoji": "💚", "style": STYLES["green"]},
    "transactions": {"emoji": "💸", "style": STYLES["cyan"]},
    "default":      {"emoji": "📩", "style": STYLES["blue"]},
}

# Colorlog setup
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(message)s",
    log_colors={
        "DEBUG":    "cyan",
        "INFO":     "white",
        "WARNING":  "yellow",
        "ERROR":    "red",
        "CRITICAL": "bold_red",
    }
))
logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


async def consume(topic: str):
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    group_id = f"test-group-{uuid.uuid4()}"

    if not bootstrap_servers:
        logger.error("KAFKA_BOOTSTRAP_SERVERS environment variable is not set.")
        return

    logger.info(f"🔌 KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")
    logger.info(f"📦 Kafka topic: {topic}")
    logger.info(f"👥 Consumer group: {group_id}")

    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset='earliest'
    )

    await consumer.start()
    try:
        logger.info(f"🧲 Subscribed to {topic}, waiting for messages...\n")
        async for msg in consumer:
            decoded = msg.value.decode('utf-8')
            partition = msg.partition
            topic_name = msg.topic

            # Determine style & emoji based on topic
            meta = TOPIC_META.get(topic_name, TOPIC_META["default"])
            emoji = meta["emoji"]
            style = meta["style"]

            # Override style if content indicates severity
            lowered = decoded.lower()
            if "error" in lowered:
                style = STYLES["red"]
            elif "warn" in lowered:
                style = STYLES["yellow"]
            elif "success" in lowered or "ok" in lowered:
                style = STYLES["green"]

            # Print the styled message
            #logger.info(f"{style}{emoji} [{topic_name}-p{partition}]: {decoded}{STYLES['reset']}")
            message_style = STYLES["yellow"]
            logger.info(f"{style}{emoji} [{topic_name}-p{partition}]: {message_style}{decoded}{STYLES['reset']}")

    except KeyboardInterrupt:
        logger.info("👋 Consumer stopped by user.")
    finally:
        await consumer.stop()
        logger.info("🛑 Kafka consumer stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Consumer")
    parser.add_argument(
        "--topic",
        type=str,
        default="test-topic",
        help="Kafka topic to consume messages from (default: test-topic)"
    )
    args = parser.parse_args()

    try:
        asyncio.run(consume(args.topic))
    except KeyboardInterrupt:
        print("\n👋 Consumer interrupted by user.")
