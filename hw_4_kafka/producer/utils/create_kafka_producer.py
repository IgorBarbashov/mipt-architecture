import json
import os
import time

from kafka import KafkaProducer

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVERS = f"{KAFKA_HOST}:{KAFKA_PORT}"


def create_producer_with_retry(retries: int = 10, delay: float = 3.0) -> KafkaProducer:
    last_err = None

    for _ in range(retries):
        try:
            return KafkaProducer(
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except Exception as e:
            last_err = e
            time.sleep(delay)
    raise last_err
