import json
from pathlib import Path
import re
import emoji

from datetime import datetime


def count_alphabetic(input_string):
    count = 0

    for char in input_string:
        if char.isalpha():
            count += 1
    return count


def count_emojis(input_string):
    count = 0

    for char in input_string:
        if emoji.EMOJI_DATA:
            count += 1
    return count


def check_message(message, MAX_TEXT_LEN, symbols_treshold=0.5):
    # remove forwarded messa
    if message.get('forwarded_from', None):
        return False

    if message.get('text', None):
        text = message.get('text', None)
        if len(text) > MAX_TEXT_LEN:
            return False
        if re.search("(?P<url>https?://[^\s]+)", str(text)):  # remove links
            return False
        alph_num = count_alphabetic(str(text))
        emoji_num = count_emojis(str(text))

        if (alph_num) / len(str(text)) < symbols_treshold:
            return False
    elif message.get('sticker_emoji', None):
        text = message.get('sticker_emoji', None)
    else:
        return False

    curr_date = datetime.strptime(
        message.get('date', None), '%Y-%m-%dT%H:%M:%S')
    curr_sender = message.get('from_id', None)

    if curr_date is None or curr_sender is None:
        return False

    return {'text': text, 'curr_date': curr_date, 'curr_sender': curr_sender}


def get_dialogues(dump_path, MAX_CONTEXT_LEN=200, MAX_TEXT_LEN=180, my_ids=['user5982387868', 'user348898603'], prompt=''):
    # MAX_CONTEXT_LEN = 500, MAX_TEXT_LEN = 200,

    with open(dump_path) as messages_file:
        messages = json.load(messages_file)['messages']

    dialogues = []
    last_post_date = None
    last_sender = None
    last_anna_text = ''

    my_text = ''
    anna_text = ''
    curr_context = ''

    for message in messages:

        message = check_message(message, MAX_TEXT_LEN)
        if not message:
            continue
        else:
            curr_date = message['curr_date']
            curr_sender = message['curr_sender']
            curr_text = message['text']

        if last_post_date == None:
            last_post_date = curr_date
        if last_sender == None:
            last_sender = curr_sender

        if curr_sender != last_sender and curr_sender not in my_ids:
            #dialogues.append({'context':curr_context, 'instruction':anna_text, 'response':my_text})
            if len(anna_text) != 0:
                curr_context += ' Собеседник:' + anna_text + '\n'
            dialogues.append({'context': curr_context, 'response': my_text})
            if len(my_text) != 0:
                curr_context += ' Ты:' + my_text + '\n'

            last_anna_text = anna_text
            anna_text = ''
            my_text = ''

        if curr_sender in my_ids:
            my_text = my_text + str(curr_text) + ' \n'
        else:
            anna_text = anna_text + str(curr_text) + ' \n'

        if len(curr_context) > MAX_CONTEXT_LEN:
            curr_context = ''

        if (curr_date - last_post_date).seconds // 3600 > 2:

            last_post_date = None
            last_sender = None

            curr_input = ''
            curr_output = ''
            curr_context = ''

        last_sender = curr_sender
        last_post_date = curr_date

        # TO-DO: catch reply_to_message_id

    return dialogues

    import os


import glob


def find_json_files(folder_path, exceptions=['']):
    json_files = []

    search_pattern = os.path.join(folder_path, '**', '*.json')

    for file_path in glob.iglob(search_pattern, recursive=True):
        if os.path.isfile(file_path) and file_path not in exceptions:
            json_files.append(file_path)

    return json_files


folder_path = '/home/box/digital_clone/dialogues'
#exceptions = ['/home/box/digital_clone/dialogues/tg_dialogues_with_anna_account_1.json']
exceptions = ['']

json_paths = find_json_files(folder_path, exceptions=exceptions)

if json_paths:
    print('-' * 110)
    print('PARSED_PATHS:')
    print('-' * 110)
    for json_file in json_paths:
        print(json_file)
else:
    print("There is no json files")


all_dialogues = []


for path in json_paths:
    # диалоги с разных аккаунтов тг
    dialogues = get_dialogues(path)

    if path == '/home/box/digital_clone/dialogues/tg_dialogues_with_anna_account_2_2.json':
        all_dialogues += dialogues[:5000]
    else:
        all_dialogues += dialogues
    print(len(dialogues))

with open('./all_dialogues.json', 'w', encoding='utf8') as json_file:
    json.dump(all_dialogues, json_file, indent=4, ensure_ascii=False)
