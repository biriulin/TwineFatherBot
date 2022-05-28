
import json

import s3
import utils
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp


class DeleteGameState(StatesGroup):
    game_name = State()

@dp.message_handler(commands=["delete"])
async def delete(message: types.Message):

    flag_user_game = await utils.choose_user_game(bot, message)
    if not flag_user_game:
        return

    await DeleteGameState.game_name.set()

@dp.message_handler(state=DeleteGameState.game_name)
async def delete_user_game(message: types.Message, state: FSMContext):
    need_stop_command = await utils.handle_stop(bot, message, state)
    if need_stop_command:
        return

    if message.text not in utils.get_user_games(message.from_user.id):
        await bot.send_message(message.from_user.id, "У тебя нет прав удалять эту игру")
        return
    
    s3.delete_files(s3_path="{}/".format(message.text))
    games_file_s3_key = "games/{}.json".format(message.from_user.id)
    try:
        user_games = json.loads(s3.get_file(games_file_s3_key))
    except:
        user_games = []
    
    user_games.remove(message.text)
    games_file_content = utils.jdump(user_games)
    s3.upload_file(games_file_content, games_file_s3_key)
    
    keyboard = utils.start_buttons()
    await bot.send_message(message.from_user.id, "Круто", reply_markup=keyboard)
    await state.finish()

def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(delete)
