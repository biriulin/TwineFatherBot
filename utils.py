import json

import requests
from aiogram import types

import config
import s3


def game_exist(game_name):
    game_file_s3_key = "{}/game_file.json".format(game_name)
    return s3.exist_file(game_file_s3_key)

def store_game_file(game_name, file, user_id):
    game_file_s3_key = "{}/game_file.json".format(game_name)
    game_file_content = jdump(take_file_content(file))
    s3.upload_file(game_file_content, game_file_s3_key)

    games_file_s3_key = "games/{}.json".format(user_id)
    try:
        user_games = json.loads(s3.get_file(games_file_s3_key))
    except:
        user_games = []

    if game_name in user_games:
        return
    
    user_games.append(game_name)
    games_file_content = jdump(user_games)
    s3.upload_file(games_file_content, games_file_s3_key)


def store_game_metadata(game_name, user_id):
    metadata_s3_key = "{}/metadata.json".format(game_name)
    metadata_content = jdump({"user_id":user_id})
    s3.upload_file(metadata_content, metadata_s3_key)

def take_file_content(file):
    file_path = take_path(file.file_id, config.TOKEN_TWINE_FATHER)
    file_content = take_file(file_path, config.TOKEN_TWINE_FATHER)
    return file_content


def jdump(text_content):
    text_content = json.dumps(text_content)
    return text_content

def take_path(file_id, token):
    response = requests.get(("https://api.telegram.org/bot{}/getFile?file_id={}").format(token, file_id))
    return response.json()['result']['file_path']

def take_file(file_path, token):
    response = requests.get(("https://api.telegram.org/file/bot{}/{}").format(token, file_path))
    return response.json()

def get_user_games(user_id):
    user_games_s3_key = "games/{}.json".format(user_id)
    try:
        user_games_content = json.loads(s3.get_file(user_games_s3_key))
        return user_games_content
    except Exception as e:
        return []

def game_file_invalid(message):
    if not message.document:
        return [False, "Это не файл дружок попробуй еще раз"]

    if message.document.file_name.split(".")[1] != "json":
        return [False, "Кажется не тот формат, отправь заново"]
    
    return [True, ""]


async def choose_user_game(bot, message):
    user_games = get_user_games(message.from_user.id)
    if not user_games:
        await bot.send_message(message.from_user.id, "У вас нет игр Дружочек")
        return False

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for game_name in user_games:
        button_game_name = types.KeyboardButton(game_name)
        keyboard.add(button_game_name)
    
    button_edit = types.KeyboardButton("/stop")
    keyboard.add(button_edit)

    await bot.send_message(message.from_user.id, "Ваши игры: {}".format(", ".join(user_games)), reply_markup=keyboard)

    return True

def start_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_create = types.KeyboardButton("/create")
    keyboard.add(button_create)
    button_delete = types.KeyboardButton("/delete")
    keyboard.add(button_delete)
    button_edit = types.KeyboardButton("/edit")
    keyboard.add(button_edit)
    button_edit = types.KeyboardButton("/start")
    keyboard.add(button_edit)
    return keyboard

def stop_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_create = types.KeyboardButton("/stop")
    keyboard.add(button_create)
    return keyboard

async def handle_stop(bot, message, state):
    if message.text == "/stop":
        await state.finish()
        key_board = start_buttons()
        await bot.send_message(message.from_user.id, "Остановлено", reply_markup=key_board)
        return True
    return False
