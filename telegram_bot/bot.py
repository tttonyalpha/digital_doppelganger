from email.mime import application
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters
from telegram import Update

from random import random

import logging
import requests

from time import sleep
from json import load, dump
from threading import Thread
from os.path import exists

from db import Database_handler

TEMPERATURE = 0.8
BOT_TOKEN = ''

if not exists("/persistent/telegram_bot/perc.json"):
    PERCENTAGES = {}
else:
    with open("/persistent/telegram_bot/perc.json", "r") as file:
        PERCENTAGES = dict(load(file))
    PERCENTAGES = {int(key): value for key, value in PERCENTAGES.items()}

db_hendler = Database_handler()
backend = "http://app:8080/predict"


async def ans_private(update: Update, context: CallbackContext):
    try:
        reply = requests.post(backend, json={
                              "input": update.message.text, "temperature": TEMPERATURE}).json()["output"]
        db_hendler.insert(update.effective_chat.id,
                          update.message.text, reply)

    except requests.exceptions.ConnectionError:
        logging.exception("ConnectionError")
        reply = "Ошибка подключения к бекенду"
        db_hendler.insert(update.effective_chat.id,
                          update.message.text, None)
        pass

    await update.message.reply_text(text=reply)
    db_hendler.flush()


async def ans_groups(update: Update, context: CallbackContext):
    if update.effective_chat.id not in PERCENTAGES.keys():
        PERCENTAGES[update.effective_chat.id] = 0.1
    perc = PERCENTAGES[update.effective_chat.id]

    if random() < perc:
        try:
            reply = requests.post(backend, json={
                                  "input": update.message.text, "temperature": TEMPERATURE}).json()["output"]

            db_hendler.insert(
                update.effective_chat.id, update.message.text, reply)

        except requests.exceptions.ConnectionError:
            logging.exception("ConnectionError")
            reply = "Ошибка подключения к бекенду"
            db_hendler.insert(
                update.effective_chat.id, update.message.text, None)
            pass

        await update.message.reply_text(text=reply)
        db_hendler.flush()


async def update_perc(update: Update, context: CallbackContext):
    global PERCENTAGES

    if update.effective_chat.id not in PERCENTAGES.keys():
        PERCENTAGES[update.effective_chat.id] = 0.1

    if len(context.args) > 0 and float(context.args[0]) >= 0 and float(context.args[0]) <= 1:
        PERCENTAGES[update.effective_chat.id] = float(context.args[0])
    await update.message.reply_text(text=f"Setting percentage {float(PERCENTAGES[update.effective_chat.id])}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()

    private_ans_handler = MessageHandler(filters.TEXT & (
        ~filters.COMMAND) & filters.ChatType.PRIVATE, ans_private)
    app.add_handler(private_ans_handler)
    groups_ans_handler = MessageHandler(filters.TEXT & (
        ~filters.COMMAND) & filters.ChatType.GROUPS, ans_groups)
    app.add_handler(groups_ans_handler)
    update_perc_handler = CommandHandler("perc", update_perc)
    app.add_handler(update_perc_handler)
    app.run_polling()


def saver():
    sleep(10)
    while True:
        with open("/persistent/telegram_bot/perc.json", "w") as file:
            dump(PERCENTAGES, file)
        sleep(10)


if __name__ == "__main__":
    saver_thread = Thread(target=saver)
    saver_thread.start()
    main()
