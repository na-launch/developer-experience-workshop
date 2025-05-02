import os
import sys
import asyncio
import argparse
import logging
import colorlog
from aiokafka import AIOKafkaProducer
from aioconsole import ainput  # For non-blocking async input

# Set up colorful logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(message)s",
    log_colors={
        "DEBUG":    "cyan",
        "INFO":     "green",
        "WARNING":  "yellow",
        "ERROR":    "red",
        "CRITICAL": "bold_red",
    }
))
logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


async def produce(topic: str):
    logger.info("Starting Kafka Producer...")
    bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")

    if not bootstrap_servers:
        logger.error("KAFKA_BOOTSTRAP_SERVERS environment variable is not set.")
        return

    logger.info(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")
    logger.info(f"Kafka topic: {topic}")

    producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    try:
        await producer.start()
    except Exception as e:
        logger.error(f"❌ Failed to start Kafka producer: {e}")
        return

    try:
        logger.info("Type your message and press Enter (type 'exit' to quit):")
        while True:
            try:
                message = await ainput("> ")
            except (EOFError, KeyboardInterrupt):
                logger.info("✋ Cancelled by user (Ctrl+C)")
                break

            message = message.strip()

            if not message:
                continue
            if message.lower() == "exit":
                break

            try:
                result = await producer.send_and_wait(topic, message.encode('utf-8'))
                logger.info(f"✅ Delivered message to {result.topic}-{result.partition}@{result.offset}")
            except Exception as e:
                logger.error(f"❌ Delivery failed: {e}")

    finally:
        await producer.stop()
        logger.info("Kafka producer stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Producer")
    parser.add_argument(
        "--topic",
        type=str,
        default="test-topic",
        help="Kafka topic to produce messages to (default: test-topic)",
    )
    args = parser.parse_args()

    async def main():
        try:
            await produce(args.topic)
        except asyncio.CancelledError:
            logger.info("✋ Cancelled by user (async)")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Producer stopped by user.")
        sys.exit(0)
