import os
import re
import logging
import logging.config
from dotenv import load_dotenv


load_dotenv()


id_pattern = re.compile(r"^.\d+$")

# vars
APP_ID = os.environ.get("APP_ID", "")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DB_URL = os.environ.get("DB_URL", "")
PICS = os.environ.get("PICS", "https://envs.sh/YB6.jpg https://envs.sh/YBy.jpg https://i.ibb.co/k6wTFbcw/file-1335.jpg https://envs.sh/YBO.jpg https://i.ibb.co/W4mJJgjR/file-1334.jpg https://envs.sh/YBg.jpg").split()
OWNER_ID = int(os.environ.get("OWNER_ID", ""))
ADMINS = [
    int(user) if id_pattern.search(user) else user
    for user in os.environ.get("ADMINS", "").split()
] + [OWNER_ID]
DB_CHANNELS = [
    int(ch) if id_pattern.search(ch) else ch
    for ch in os.environ.get("DB_CHANNELS", "").split()
]

#try:
#import const
#except Exception:
import sample_const as const

START_MSG = const.STARTMSG
START_KB = const.START_KB
HELP_MSG = const.HELPMSG
HELP_KB = const.HELP_KB


# logging Conf
logging.config.fileConfig(fname="config.ini", disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)



from aiohttp import web
from .route import routes


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
