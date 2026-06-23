"""
handlers/support.py
24/7 колдоо бөлүмү.
"""
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database import Database
from locales import L
from config import SUPPORT_CONTACT
from keyboards import kb_back_to_main
from subscription import require_subscription

router = Router(name="support")


@router.callback_query(F.data == "menu_support")
async def show_support(callback: CallbackQuery, db: Database, bot: Bot):
    lang = await db.get_language(callback.from_user.id)
    await callback.answer()
    if not await require_subscription(callback, bot, lang):
        return

    text = L["support_text"][lang].format(contact=SUPPORT_CONTACT)
    await callback.message.edit_text(text, reply_markup=kb_back_to_main(lang))
