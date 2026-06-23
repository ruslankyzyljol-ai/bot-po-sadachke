"""
handlers/start.py
/start командасы, тил тандоо, башкы менюга кайтуу.
"""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from database import Database
from locales import L
from keyboards import kb_language, kb_main_menu
from subscription import is_subscribed_to_all, send_not_subscribed

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database, bot: Bot):
    is_new = await db.add_user_if_not_exists(
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name or "",
    )
    lang = await db.get_language(message.from_user.id)

    if lang is None:
        # Тил эч качан тандалган эмес - тил тандоодон баштайбыз
        await message.answer(L["choose_language"]["ky"], reply_markup=kb_language())
        return

    await enter_main_flow(message, db, bot, lang)


@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_language(callback: CallbackQuery, db: Database, bot: Bot):
    lang = callback.data.split(":")[1]
    await db.set_language(callback.from_user.id, lang)
    await callback.answer()
    await enter_main_flow(callback, db, bot, lang)


@router.callback_query(F.data == "menu_language")
async def cb_change_language(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(L["choose_language"]["ky"], reply_markup=kb_language())


@router.callback_query(F.data == "check_sub")
async def cb_check_subscription(callback: CallbackQuery, db: Database, bot: Bot):
    lang = await db.get_language(callback.from_user.id)
    if await is_subscribed_to_all(bot, callback.from_user.id):
        await callback.answer(L["subscribed_success"][lang], show_alert=True)
        await show_main_menu(callback, lang)
    else:
        await callback.answer(L["still_not_subscribed_alert"][lang], show_alert=True)


@router.callback_query(F.data == "menu_main")
async def cb_back_to_main(callback: CallbackQuery, db: Database, bot: Bot):
    lang = await db.get_language(callback.from_user.id)
    await callback.answer()
    await enter_main_flow(callback, db, bot, lang)


async def enter_main_flow(event, db: Database, bot: Bot, lang: str):
    """Ар бир кирүүдө катталуусун кайра текшерет."""
    user_id = event.from_user.id
    if await is_subscribed_to_all(bot, user_id):
        await show_main_menu(event, lang)
    else:
        await send_not_subscribed(event, lang)


async def show_main_menu(event, lang: str):
    text = L["main_menu_text"][lang]
    kb = kb_main_menu(lang, event.from_user.id)
    if isinstance(event, CallbackQuery):
        try:
            await event.message.edit_text(text, reply_markup=kb)
        except Exception:
            await event.message.answer(text, reply_markup=kb)
    else:
        await event.answer(text, reply_markup=kb)
