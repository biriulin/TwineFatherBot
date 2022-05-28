import logging

from aiogram import executor

from create_bot import dp
from handlers import commands, create, delete, edit, start

logging.basicConfig(level=logging.INFO)

commands.register_message_handler(dp)
start.register_message_handler(dp)
create.register_message_handler(dp)
delete.register_message_handler(dp)
edit.register_message_handler(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
