"""
keyboards.py
Бардык inline баскычтар (клавиатуралар) ушул жерде курулат.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNELS, ADMIN_IDS
from locales import L
from courses_data import COURSES


def kb_language() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🇰🇬 Кыргызча", callback_data="set_lang:ky")
    b.button(text="🇷🇺 Русский", callback_data="set_lang:ru")
    b.adjust(2)
    return b.as_markup()


def kb_subscribe(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for ch in CHANNELS:
        b.button(text="📢 " + ch["title"][lang], url=ch["url"])
    b.button(text=L["check_button"][lang], callback_data="check_sub")
    b.adjust(1)
    return b.as_markup()


def kb_main_menu(lang: str, user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=L["btn_courses"][lang], callback_data="menu_courses")
    b.button(text=L["btn_support"][lang], callback_data="menu_support")
    b.button(text=L["btn_language"][lang], callback_data="menu_language")
    if user_id in ADMIN_IDS:
        b.button(text=L["btn_admin"][lang], callback_data="menu_admin")
    b.adjust(1)
    return b.as_markup()


def kb_back_to_main(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=L["btn_back"][lang], callback_data="menu_main")
    return b.as_markup()


def kb_courses_list(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for idx, lesson in enumerate(COURSES[lang]):
        b.button(text=lesson["title"], callback_data=f"lesson:{idx}")
    b.button(text=L["btn_back"][lang], callback_data="menu_main")
    b.adjust(1)
    return b.as_markup()


def kb_lesson_nav(lang: str, idx: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    total = len(COURSES[lang])
    row = []
    if idx > 0:
        b.button(text="⬅️", callback_data=f"lesson:{idx - 1}")
    if idx < total - 1:
        b.button(text="➡️", callback_data=f"lesson:{idx + 1}")
    b.button(text=L["btn_back"][lang], callback_data="menu_courses")
    b.adjust(2, 1)
    return b.as_markup()


def kb_admin_panel(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=L["btn_broadcast"][lang], callback_data="admin_broadcast")
    b.button(text=L["btn_stats"][lang], callback_data="admin_stats")
    b.button(text=L["btn_back"][lang], callback_data="menu_main")
    b.adjust(1)
    return b.as_markup()
