FROM python:3.14-slim

WORKDIR /home/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ms-hello.py /home/app/

CMD fastapi run /home/app/ms-hello.py --host 0.0.0.0 --port $MS_HELLO_CONTAINER_PORT
