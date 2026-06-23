# config.py
# Бул жерде сырлуу маалыматтар (токен, админ ID) ENVIRONMENT VARIABLE'дан
# окулат - алар GitHub'ка эч качан ачык жазылбайт. Локалдык компьютерде
# сынаганда .env файлын колдонсоңуз болот (README'де көрсөтүлгөн).
#
# Render.com'до бул маанилерди "Environment" бөлүмүнөн (сайт аркылуу) жазасыз.

import os

# Жергиликтүү компьютерде сынаганда .env файлынан жүктөө үчүн (милдеттүү эмес)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


# 1) BotFather'дан алган бот токени (ENV: BOT_TOKEN)
BOT_TOKEN = _get_env("BOT_TOKEN", "СЕНИН_БОТ_ТОКЕНИН_БУЛ_ЖЕРГЕ_ЖАЗ")

# 2) Админдердин Telegram ID'лери, үтүр менен бөлүнгөн (ENV: ADMIN_IDS)
#    Мисал: ADMIN_IDS=111111111,222222222
#    Өзүңүздүн ID'иңизди билбесеңиз, @userinfobot ботуна жазыңыз
_admin_ids_raw = _get_env("ADMIN_IDS", "6954551561")
ADMIN_IDS = [int(x.strip()) for x in _admin_ids_raw.split(",") if x.strip()]

# 3) Катталуу милдеттүү болгон 3 канал
#    chat_id - канал @username же -100... түрүндөгү ID болушу мүмкүн
#    url - колдонуучу басып каналга өтө турган шилтеме
#    !!! БОТ ОШОЛ КАНАЛДАРГА АДМИН БОЛУП КОШУЛГАН БОЛУШУ КЕРЕК,
#        болбосо подпискасын текшере албайт !!!
#    Бул тизме сыр эмес, андыктан коддун ичинде кала берет - өзгөртүү
#    керек болсо ушул жерден түз эле өзгөртөсүз.
CHANNELS = [
    {
        "chat_id": "@profixkg",
        "url": "https://t.me/profixkg",
        "title": {"ky": "1-канал", "ru": "1-й канал"},
    },
    {
        "chat_id": "@sarabotikkg",
        "url": "https://t.me/sarabotikkg",
        "title": {"ky": "2-канал", "ru": "2-й канал"},
    },
    {
        "chat_id": "@muzik55tt",
        "url": "https://t.me/muzik55tt",
        "title": {"ky": "3-канал", "ru": "3-й канал"},
    },
]

# 4) Колдоо (поддержка) үчүн контакт - @username же телефон (ENV: SUPPORT_CONTACT)
SUPPORT_CONTACT = _get_env("SUPPORT_CONTACT", "@your_support_username")

# 5) Маалымат базасынын файлы (өзгөртпөй коюуга болот)
DB_PATH = "bot.db"
