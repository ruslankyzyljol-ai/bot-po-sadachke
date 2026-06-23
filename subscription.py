"""
subscription.py
Колдонуучунун 3 каналга катталганын текшерген жардамчы функциялар.
Бул модуль handler эмес — башка handler'лер ичинен чакырылат.
"""
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message, CallbackQuery

from config import CHANNELS
from locales import L
from keyboards import kb_subscribe

NOT_SUBSCRIBED_STATUSES = {"left", "kicked"}


async def is_subscribed_to_all(bot: Bot, user_id: int) -> bool:
    """Бардык талап кылынган каналдарга катталганын текшерет."""
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch["chat_id"], user_id)
            if member.status in NOT_SUBSCRIBED_STATUSES:
                return False
        except (TelegramBadRequest, TelegramForbiddenError):
            # Бот ошол каналда админ эмес болсо же канал табылбаса,
            # коопсуздук үчүн "катталган эмес" деп эсептейбиз.
            return False
    return True


async def send_not_subscribed(event: Message | CallbackQuery, lang: str):
    text = L["not_subscribed"][lang]
    kb = kb_subscribe(lang)
    if isinstance(event, CallbackQuery):
        try:
            await event.message.edit_text(text, reply_markup=kb)
        except TelegramBadRequest:
            await event.message.answer(text, reply_markup=kb)
        await event.answer()
    else:
        await event.answer(text, reply_markup=kb)


async def require_subscription(event: Message | CallbackQuery, bot: Bot, lang: str) -> bool:
    """
    Протекцияланган бөлүмдөрдүн (курстар, колдоо ж.б.) башында чакырылат.
    True кайтарса - колдонуучу катталган, улантса болот.
    False кайтарса - "катталган эмес" билдирүүсү жөнөтүлдү, handler токтошу керек.
    """
    user_id = event.from_user.id
    if await is_subscribed_to_all(bot, user_id):
        return True
    await send_not_subscribed(event, lang)
    return False
