import utils
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp


class CreateGameState(StatesGroup):
    game_name = State()
    game_file = State()

@dp.message_handler(commands=["create"])
async def create(message: types.Message):
    keyboard = utils.stop_button()
    await bot.send_message(message.from_user.id, "Название", reply_markup=keyboard)
    await CreateGameState.game_name.set()


@dp.message_handler(state=CreateGameState.game_name)
async def process_game_name(message: types.Message, state: FSMContext):
    need_stop_command = await utils.handle_stop(bot, message, state)
    if need_stop_command:
        return

    if utils.game_exist(game_name=message.text):
        await bot.send_message(message.from_user.id, "Уже есть такой")
        return

    async with state.proxy() as data:
        data["game_name"] = message.text

    utils.store_game_metadata(game_name=message.text, user_id=message.from_user.id)

    await bot.send_message(message.from_user.id, "Теперь отправь мне файл")
    await CreateGameState.game_file.set()

@dp.message_handler(state=CreateGameState.game_file)
@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=CreateGameState.game_file)
async def process_game_file(message: types.Message, state: FSMContext):
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
    await bot.send_message(message.from_user.id, "TY", reply_markup=keyboard)
    await state.finish()

def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(create)

