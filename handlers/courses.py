"""
handlers/courses.py
Сабактар бөлүмү: тизме жана ар бир сабактын толук тексти + YouTube видео.
"""
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database import Database
from locales import L
from courses_data import COURSES
from keyboards import kb_courses_list, kb_lesson_nav
from subscription import require_subscription

router = Router(name="courses")


@router.callback_query(F.data == "menu_courses")
async def show_courses_list(callback: CallbackQuery, db: Database, bot: Bot):
    lang = await db.get_language(callback.from_user.id)
    await callback.answer()
    if not await require_subscription(callback, bot, lang):
        return
    await callback.message.edit_text(
        L["courses_title"][lang], reply_markup=kb_courses_list(lang)
    )


@router.callback_query(F.data.startswith("lesson:"))
async def show_lesson(callback: CallbackQuery, db: Database, bot: Bot):
    lang = await db.get_language(callback.from_user.id)
    await callback.answer()
    if not await require_subscription(callback, bot, lang):
        return

    idx = int(callback.data.split(":")[1])
    lesson = COURSES[lang][idx]

    text = (
        f"<b>{lesson['title']}</b>\n\n"
        f"{lesson['text']}\n\n"
        f"{L['lesson_youtube'][lang]}: {lesson['youtube']}"
    )
    await callback.message.edit_text(text, reply_markup=kb_lesson_nav(lang, idx))
