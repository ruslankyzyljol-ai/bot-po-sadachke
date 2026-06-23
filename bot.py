"""
bot.py
Ботту иштетүүчү негизги файл. Иштетүү үчүн: python bot.py

Render'дин БЕКЕР тарифи (Web Service) HTTP портун күтөт, андыктан бул
файлда Telegram polling'ге кошумча кичинекей веб-сервер да ачылат
("/" жана "/health" жолдору). UptimeRobot сыяктуу кызмат ага ар бир
5-10 мүнөт сайын кирип турса, Render аны "уктатпай" кармайт.
"""
import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DB_PATH
from database import Database
from handlers import start, courses, support, admin


async def handle_ping(request):
    return web.Response(text="MoneyBot иштеп турат ✅")


async def run_web_server():
    """Render'дин талап кылган портунда жөнөкөй HTTP сервер ачат."""
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)

    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    logging.info(f"Веб-сервер {port}-портто ачылды (UptimeRobot үчүн)")


async def main():
    logging.basicConfig(level=logging.INFO)

    if BOT_TOKEN == "СЕНИН_БОТ_ТОКЕНИН_БУЛ_ЖЕРГЕ_ЖАЗ":
        raise RuntimeError(
            "BOT_TOKEN табылбады! Локалда .env файлына, Render'де "
            "Environment Variables бөлүмүнө BOT_TOKEN жазыңыз "
            "(@BotFather'дан алган чыныгы токен болушу керек)."
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
        await run_web_server()
        logging.info("Бот иштеп баштады...")
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
