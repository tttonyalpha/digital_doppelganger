import torch
import transformers
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pandas as pd
import sentence_transformers
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, GPT2Tokenizer
from peft import PeftModel, PeftConfig, LoraConfig, get_peft_model, prepare_model_for_int8_training, TaskType

from sentence_transformers import SentenceTransformer,
from sentence_transformers.util import cos_sim

import asyncio
import nest_asyncio
nest_asyncio.apply()

pre_prompt = 'Тебя зовут Никита, тебе 21 год. Ты учишься на 3-ем курсе ВШЭ и занимаешься машинным обучением. Ты общаешься со своим другом, напиши ответ на его сообщение. '
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = GPT2Tokenizer.from_pretrained(
    "ai-forever/FRED-T5-1.7B")
model = T5ForConditionalGeneration.from_pretrained(
    "ai-forever/FRED-T5-1.7B", load_in_8bit=True, device_map="auto")
tokenizer.add_special_tokens(
    {'bos_token': '<s>', 'eos_token': '</s>', 'pad_token': '<pad>'})
sentence_model = SentenceTransformer(
    'sentence-transformers/distiluse-base-multilingual-cased-v1')

peft_model_id = "PATH_TO_CHECKPOINT"

config = PeftConfig.from_pretrained(peft_model_id)
peft_trained_model = PeftModel.from_pretrained(
    model, peft_model_id, device_map="auto", torch_dtype=torch.float32)
peft_trained_model.eval()


pre_prompt = 'Тебя зовут Никита, тебе 21 год. Ты учишься на 3-ем курсе ВШЭ и занимаешься машинным обучением. Ты общаешься со своим другом, напиши ответ на его сообщение. '

knowlodge_base_path = "KNOWLEDGE_BASE_PATH"
knowledge_base = pd.read_csv(knowlodge_base_path)


bot_prefix = '!'
bot = Bot(token='BOT_TOKEN')
dp = Dispatcher(bot)

dialog = []
user_messages = {}


@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    response = 'Привет! Я цифровой двойник Никиты: @my_name_is_nikita_hey Напиши мне что-нибудь :)'
    await message.answer(response)


@dp.message_handler()
async def message_handler(message: types.Message):

    user_id = message.from_user.id
    text = message.text

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(text)

    global dialog
    print(dialog)
    await asyncio.sleep(5)

    if user_id in user_messages and len(user_messages[user_id]) > 0:

        user_msg = "\n".join(user_messages[user_id])
        if len(dialog) > 10:
            dialog = []

        dialog.append('Собеседник: ' + user_msg)

        fact, fact_score = get_best_fact(user_msg)
        best_response = fact

        bot_response = generate_response(user_msg, dialog)
        bot_score = get_relevance(bot_response, user_msg)

        if bot_score - fact_score > 0.1:
            best_response = bot_response

        dialog.append('Никита: ' + best_response)
        user_messages[user_id] = []

        for el in best_response.split('\n'):
            await message.answer(el)


def get_relevance(sentence_1, sentence_2):
    embeddings = sentence_model.encode([sentence_1, sentence_2])
    return cos_sim(a=embeddings[0], b=embeddings[1])


def get_best_fact(user_msg):
    global knowledge_base

    knowledge_base['score'] = knowledge_base.fact.apply(
        lambda x: get_relevance(x, user_msg)[0][0].numpy())

    best_id = knowledge_base['score'].idxmax()
    best_fact = knowledge_base.iloc[best_id].fact
    best_score = knowledge_base.iloc[best_id].score

    return best_fact, best_score


def generate_response(user_msg, dialog):
    print(user_msg)
    prompt = '<SC1>' + pre_prompt + 'Ваш прошлый диалог:' + \
        '\n'.join(dialog) + ' Твой ответ:<extra_id_0>'
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to(device)
    out_ids = peft_trained_model.generate(input_ids=input_ids,
                                          max_length=30,
                                          eos_token_id=tokenizer.eos_token_id,
                                          early_stopping=True,
                                          do_sample=True,
                                          temperature=0.8,
                                          num_beams=3,
                                          top_k=50,
                                          top_p=0.85)
    t5_output = tokenizer.decode(out_ids[0][1:]).replace('<extra_id_0>', '')
    if '</s>' in t5_output:
        t5_output = t5_output[:t5_output.find('</s>')].strip()
    return t5_output


async def on_startup(dp):
    print('hi')


async def on_shutdown(dp):
    print('biy')
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)
