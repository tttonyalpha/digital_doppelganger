FROM python: 3.7

RUN apt - get update & & \
    apt - get install nginx - y & & \
    pip3 install supervisor

COPY requirements.txt .
RUN pip3 install - r requirements.txt

RUN mkdir / app
WORKDIR / app

RUN mkdir / prom

COPY supervisord.conf / etc / supervisord.conf
COPY config.nginx / etc / config.nginx

COPY app.py gunicorn.py model.py / app/

ENTRYPOINT["supervisord", "-c", "/etc/supervisord.conf"]
