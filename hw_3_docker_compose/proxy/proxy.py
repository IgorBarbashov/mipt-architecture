"""
Proxy-сервис - вызывает внутренний микросервис и отдает клиенту полученные от него данные
"""

import os

import requests
from fastapi import FastAPI

app = FastAPI()

MS_HELLO_HOST = os.getenv("MS_HELLO_HOST")
MS_HELLO_CONTAINER_PORT = os.getenv("MS_HELLO_CONTAINER_PORT")
MS_HELLO_BASE_URL = f"http://{MS_HELLO_HOST}:{MS_HELLO_CONTAINER_PORT}"


@app.get("/proxy")
def gateway():
    resp = requests.get(f"{MS_HELLO_BASE_URL}/hello")
    return resp.json()
