"""
bot.py
Ботту иштетүүчү негизги файл. Иштетүү үчүн: python bot.py
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DB_PATH
from database import Database
from handlers import start, courses, support, admin


async def main():
    logging.basicConfig(level=logging.INFO)

    if BOT_TOKEN == "СЕНИН_БОТ_ТОКЕНИН_БУЛ_ЖЕРГЕ_ЖАЗ":
        raise RuntimeError(
            "config.py файлындагы BOT_TOKEN'ди @BotFather'дан алган "
            "чыныгы токенге алмаштырыңыз!"
        )

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    db = Database(DB_PATH)
    await db.init()

    # db бардык handler'лерге аргумент катары автоматтык түрдө берилет
    dp["db"] = db

    dp.include_router(start.router)
    dp.include_router(courses.router)
    dp.include_router(support.router)
    dp.include_router(admin.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Бот иштеп баштады...")
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
