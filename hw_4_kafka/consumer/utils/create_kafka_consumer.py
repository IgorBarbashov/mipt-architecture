import os
import time

from kafka import KafkaConsumer, TopicPartition

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_PARTITION = int(os.getenv("KAFKA_PARTITION", "0"))
KAFKA_BOOTSTRAP_SERVERS = f"{KAFKA_HOST}:{KAFKA_PORT}"


def create_consumer_with_retry(retries: int = 10, delay: float = 3.0) -> KafkaConsumer:
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            c = KafkaConsumer(
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                auto_offset_reset="latest",
                enable_auto_commit=False,
            )
            partition = TopicPartition(KAFKA_TOPIC, KAFKA_PARTITION)
            c.assign([partition])
            return c
        except Exception as e:
            last_err = e
            time.sleep(delay)
    assert last_err is not None
    raise last_err
