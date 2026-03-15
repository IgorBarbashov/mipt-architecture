import json

from db import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from kafka import TopicPartition
from models.errors import Errors
from sqlalchemy.orm import Session
from utils.create_kafka_consumer import (
    KAFKA_PARTITION,
    KAFKA_TOPIC,
    create_consumer_with_retry,
)

app = FastAPI()

consumer = None
tp = None


@app.on_event("startup")
def on_startup():
    global consumer, tp
    Base.metadata.create_all(bind=engine)
    consumer = create_consumer_with_retry()
    tp = TopicPartition(KAFKA_TOPIC, KAFKA_PARTITION)


@app.get("/last")
def get_last_message(db: Session = Depends(get_db)):
    if consumer is None or tp is None:
        raise HTTPException(status_code=503, detail="Kafka consumer not initialized")

    end_offsets = consumer.end_offsets([tp])
    last_offset = end_offsets[tp]

    if last_offset == 0:
        return {"message": None}

    consumer.seek(tp, last_offset - 1)
    msg = next(consumer)

    raw_value = msg.value.decode("utf-8", errors="replace")

    try:
        data = json.loads(raw_value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in Kafka message")

    db_error = Errors(
        code=data.get("code"),
        message=data.get("message"),
        details=data.get("details"),
    )

    db.add(db_error)
    db.commit()
    db.refresh(db_error)

    return {
        "topic": msg.topic,
        "partition": msg.partition,
        "offset": msg.offset,
        "value": msg.value.decode("utf-8", errors="replace"),
    }
