FROM python:3.7

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir /telegram_bot
WORKDIR /telegram_bot

COPY bot.py db.py /telegram_bot/

ENTRYPOINT ["python3", "bot.py"]