import utils
from aiogram import Dispatcher, types
from create_bot import bot, dp


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = utils.start_buttons()

    await bot.send_message(message.from_user.id,"Привет! Если ты зашел ко мне, то решил создать свою игру :o\nСейчас я расскажу что надо делать.\n")
    await bot.send_message(message.from_user.id,"Зайди на сайт https://twinery.org/2. Нажми на кнопку формат и добавь новый по ссылке https://jtschoonhoven.github.io/twine-to-json/dist/harlowe-3.js")
    await bot.send_message(message.from_user.id,"Теперь нажми на кнопку +История и создай свою цепочку дейсвтвий главного героя")
    await bot.send_message(message.from_user.id,"После этого нажми на навание своей истори снизу слева и поменяй формат истории на Harlowe 3 to JSON и нажми опубликовать в файл")
    await bot.send_message(message.from_user.id,"Нажми на кнопку 'Создать игру' и отправь файл.json.")
    await bot.send_message(message.from_user.id,"Готово, твоя игра появилась в боте ...", reply_markup=keyboard)


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(start)
