FROM python:3.14-slim

WORKDIR /home/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./proxy.py /home/app/

CMD fastapi run /home/app/proxy.py --host 0.0.0.0 --port $PROXY_CONTAINER_PORT