import utils
from aiogram import Dispatcher, types
from create_bot import bot, dp


@dp.message_handler(commands=["commands"])
async def commands(message: types.Message):
    keyboard = utils.start_buttons()
    await bot.send_message(message.from_user.id,"Команды на кнопках", reply_markup=keyboard)

def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(commands)
