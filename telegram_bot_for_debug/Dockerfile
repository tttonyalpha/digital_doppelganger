FROM python:3.7

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY bot.py /app/bot.py

CMD ["python", "bot.py"]