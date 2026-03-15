FROM python:3.14-slim

WORKDIR /home/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/app

CMD uvicorn consumer:app --host 0.0.0.0 --port $CONSUMER_CONTAINER_PORT
