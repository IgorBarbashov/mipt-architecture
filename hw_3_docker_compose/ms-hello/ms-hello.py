"""
Микросервис, доступен только внутри docker
Отвечает на GET-запрос по внутренней сети
"""

import os

from fastapi import FastAPI

app = FastAPI()

MS_HELLO_HOST = os.getenv("MS_HELLO_HOST")


@app.get("/hello")
async def hello():
    return {"message": f"Hello from {MS_HELLO_HOST} microservice"}
