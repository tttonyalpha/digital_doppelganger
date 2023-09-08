import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.types import ContentType
from aiogram.utils import markdown as md
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


tokenizer = transformers.GPT2Tokenizer.from_pretrained(
    "ai-forever/FRED-T5-1.7B")
model = transformers.T5ForConditionalGeneration.from_pretrained(
    "ai-forever/FRED-T5-1.7B", load_in_8bit=True, device_map="auto")
tokenizer.add_special_tokens(
    {'bos_token': '<s>', 'eos_token': '</s>', 'pad_token': '<pad>'})


checkpoint = 'PATH_TO_CHECKPOINT'

peft_trained_model = PeftModel.from_pretrained(
    model, checkpoint, device_map="auto", torch_dtype=torch.float16)
peft_trained_model.eval()


bot = Bot(token='BOT_TOKEN')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


class DialogStates(StatesGroup):
    waiting_for_message = State()


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет, я цифровая копия Никиты: https://t.me/\n Напиши мне что-нибудь!")


@dp.message_handler(state=DialogStates.waiting_for_message, content_types=ContentType.TEXT)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['dialog'].append(message.text)

        pre_prompt = 'Тебя зовут Никита, тебе 21 год. Ты учишься на 3-ем курсе ВШЭ и занимаешься машинным обучением. Ты общаешься со своим другом, напиши ответ на его сообщение. '
        prompt = '<SC1>' + pre_prompt + 'Ваш прошлый диалог:' + \
            '\n'.join(data['dialog']) + ' Твой ответ:<extra_id_0>'

        input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to(device)
        out_ids = peft_trained_model.generate(input_ids=input_ids,
                                              max_length=50,
                                              eos_token_id=tokenizer.eos_token_id,
                                              early_stopping=True,
                                              do_sample=True,
                                              temperature=0.8,
                                              top_k=50,
                                              top_p=0.85)

        t5_output = tokenizer.decode(
            out_ids[0][1:]).replace('<extra_id_0>', '')
        if '</s>' in t5_output:
            t5_output = t5_output[:t5_output.find('</s>')].strip()

        data['dialog'].append('Никита: ' + t5_output)
        await message.answer('Никита: {}'.format(t5_output))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
