"""
handlers/admin.py
Админ панели: бардык колдонуучуларга билдирүү жөнөтүү (текст/фото/видео/документ),
колдонуучулар санын көрүү.
"""
import asyncio
from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from database import Database
from locales import L
from config import ADMIN_IDS
from keyboards import kb_admin_panel, kb_back_to_main

router = Router(name="admin")


class BroadcastState(StatesGroup):
    waiting_content = State()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.callback_query(F.data == "menu_admin")
async def open_admin_panel(callback: CallbackQuery, db: Database):
    lang = await db.get_language(callback.from_user.id)
    if not _is_admin(callback.from_user.id):
        await callback.answer(L["admin_only"][lang], show_alert=True)
        return
    await callback.answer()
    await callback.message.edit_text(
        L["admin_panel_text"][lang], reply_markup=kb_admin_panel(lang)
    )


@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery, db: Database):
    lang = await db.get_language(callback.from_user.id)
    if not _is_admin(callback.from_user.id):
        await callback.answer(L["admin_only"][lang], show_alert=True)
        return
    count = await db.count_users()
    await callback.answer()
    await callback.message.edit_text(
        L["stats_text"][lang].format(count=count),
        reply_markup=kb_admin_panel(lang),
    )


@router.callback_query(F.data == "admin_broadcast")
async def ask_broadcast_content(callback: CallbackQuery, db: Database, state: FSMContext):
    lang = await db.get_language(callback.from_user.id)
    if not _is_admin(callback.from_user.id):
        await callback.answer(L["admin_only"][lang], show_alert=True)
        return
    await callback.answer()
    await state.set_state(BroadcastState.waiting_content)
    await state.update_data(lang=lang)
    await callback.message.edit_text(
        L["broadcast_prompt"][lang], reply_markup=kb_back_to_main(lang)
    )


@router.message(Command("cancel"), StateFilter(BroadcastState.waiting_content))
async def cancel_broadcast(message: Message, db: Database, state: FSMContext):
    lang = await db.get_language(message.from_user.id)
    await state.clear()
    await message.answer(L["broadcast_cancelled"][lang], reply_markup=kb_back_to_main(lang))


@router.message(StateFilter(BroadcastState.waiting_content))
async def do_broadcast(message: Message, db: Database, bot: Bot, state: FSMContext):
    """
    Админ жөнөткөн билдирүүнү (текст/фото/видео/документ/ — каалаганын)
    бардык колдонуучуларга copy_message менен жөнөтөт.
    """
    if not _is_admin(message.from_user.id):
        return

    data = await state.get_data()
    lang = data.get("lang", "ky")
    await state.clear()

    await message.answer(L["broadcast_started"][lang])

    user_ids = await db.get_all_user_ids()
    ok, fail = 0, 0

    for uid in user_ids:
        try:
            await bot.copy_message(
                chat_id=uid,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            ok += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            fail += 1
        # Telegram'дын лимиттерине урунбоо үчүн кичине тыныгуу
        await asyncio.sleep(0.05)

    await message.answer(
        L["broadcast_done"][lang].format(ok=ok, fail=fail),
        reply_markup=kb_admin_panel(lang),
    )
