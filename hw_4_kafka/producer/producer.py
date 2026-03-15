from fastapi import FastAPI
from kafka import KafkaProducer
from schemas.errors import Errors
from utils.create_kafka_producer import KAFKA_TOPIC, create_producer_with_retry

app = FastAPI()
producer: KafkaProducer | None = None


@app.on_event("startup")
def startup_event():
    global producer
    producer = create_producer_with_retry()


@app.post("/errors")
async def produce(error: Errors):
    assert producer is not None, "Kafka producer not initialized"
    payload = error.model_dump()
    producer.send(KAFKA_TOPIC, value=payload)
    producer.flush()
    return {"status": "ok"}
