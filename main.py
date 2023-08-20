from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.parser import check_data
from aiogram import Bot, Dispatcher, executor
from app import database as db
from config import token
import asyncio
import os

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')
    asyncio.create_task(periodic_check())


async def periodic_check():
    while True:
        await asyncio.sleep(5)
        result_text = check_data()
        if result_text:
            user_ids = await db.mailing()
            for user_id in user_ids:
                await bot.send_message(user_id[0], result_text)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)