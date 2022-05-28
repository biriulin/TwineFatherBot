import utils
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp


class EditGameState(StatesGroup):
    game_name = State()
    edit_field = State()
    edit_game_file = State()
    edit_game_name = State()


@dp.message_handler(commands=["edit"])
async def edit(message: types.Message):
    flag_user_game = await utils.choose_user_game(bot, message)
    if not flag_user_game:
        return
    await EditGameState.game_name.set()

@dp.message_handler(state=EditGameState.game_name)
async def take_game_name(message: types.Message, state: FSMContext):
    need_stop_command = await utils.handle_stop(bot, message, state)
    if need_stop_command:
        return
    
    if message.text not in utils.get_user_games(message.from_user.id):
        await bot.send_message(message.from_user.id, "У тебя нет прав редактировать эту игру")
        return

    async with state.proxy() as data:
        data["game_name"] = message.text

    key_board = utils.stop_button()

    await bot.send_message(message.from_user.id, "Отправь мне файл", reply_markup=key_board)
    await EditGameState.edit_game_file.set()


@dp.message_handler(state=EditGameState.edit_game_file)
@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=EditGameState.edit_game_file)
async def get_game_file(message: types.Message, state: FSMContext):
    need_stop_command = await utils.handle_stop(bot, message, state)
    if need_stop_command:
        return

    [invalid, message_for_user] = utils.game_file_invalid(message)
    if not invalid:
        await bot.send_message(message.from_user.id, message_for_user)
        return
    

    async with state.proxy() as data:
        utils.store_game_file(game_name=data["game_name"], file=message.document, user_id=message.from_user.id)

    keyboard = utils.start_buttons()
    await bot.send_message(message.from_user.id, "Отредактировал Файл", reply_markup=keyboard)
    await state.finish()

def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(edit)
