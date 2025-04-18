import os
import sys
import asyncio
import time
import shutil
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from psutil import cpu_percent, virtual_memory, disk_usage
from pyrogram import Client, filters, enums
from mfinder.db.broadcast_sql import add_user
from mfinder.db.settings_sql import get_search_settings, change_search_settings, get_channel
from mfinder.utils.constants import STARTMSG, HELPMSG
from mfinder import LOGGER, ADMINS, START_MSG, HELP_MSG, START_KB, HELP_KB
from mfinder.utils.util_support import humanbytes, get_db_size
from mfinder.plugins.serve import get_files
from .serve import is_subscribed

@Client.on_message(filters.command(["start"]))
async def start(bot, update):
    if len(update.command) == 1:
        user_id = update.from_user.id
        name = update.from_user.first_name if update.from_user.first_name else " "
        user_name = (
            "@" + update.from_user.username if update.from_user.username else None
        )
        await add_user(user_id, user_name)

        try:
            start_msg = START_MSG.format(name, user_id)
        except Exception as e:
            LOGGER.warning(e)
            start_msg = STARTMSG.format(name, user_id)

        await bot.send_message(
            chat_id=update.chat.id,
            text=start_msg,
            reply_to_message_id=update.reply_to_message_id,
            reply_markup=START_KB,
        )
        search_settings = await get_search_settings(user_id)
        if not search_settings:
            await change_search_settings(user_id, button_mode=True)
    elif len(update.command) == 2:
        force_sub = await get_channel()
        if force_sub:
            try:
                if not await is_subscribed(bot, update):
                    link = await bot.create_chat_invite_link(int(force_sub), creates_join_request=True)
                    await update.reply_text(
                        text="**Pʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴩᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴜꜱɪɴɢ ʙᴏᴛ !** 😶‍🌫️",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("❃ Jᴏɪɴ ❃", url=link.invite_link)]]
                        ),
                        parse_mode=enums.ParseMode.MARKDOWN,
                        quote=True,
                    )
                    return
            except Exception as e:
                LOGGER.warning(e)
                await update.reply_text(
                    text="Something went wrong, please contact my support group",
                    quote=True,
                )
                return
        await get_files(bot, update)


@Client.on_message(filters.command(["help"]))
async def help_m(bot, update):
    try:
        help_msg = HELP_MSG
    except Exception as e:
        LOGGER.warning(e)
        help_msg = HELPMSG

    await bot.send_message(
        chat_id=update.chat.id,
        text=help_msg,
        reply_to_message_id=update.reply_to_message_id,
        reply_markup=HELP_KB,
    )


@Client.on_callback_query(filters.regex(r"^back_m$"))
async def back(bot, query):
    user_id = query.from_user.id
    name = query.from_user.first_name if query.from_user.first_name else " "
    try:
        start_msg = START_MSG.format(name, user_id)
    except Exception as e:
        LOGGER.warning(e)
        start_msg = STARTMSG
    await query.message.edit_text(start_msg, reply_markup=START_KB)


@Client.on_callback_query(filters.regex(r"^help_cb$"))
async def help_cb(bot, query):
    try:
        help_msg = HELP_MSG
    except Exception as e:
        LOGGER.warning(e)
        help_msg = HELPMSG
    await query.message.edit_text(help_msg, reply_markup=HELP_KB)


@Client.on_message(filters.command(["restart"]) & filters.user(ADMINS))
async def restart(bot, update):
    LOGGER.warning("Restarting bot using /restart command")
    msg = await update.reply_text(text="__Restarting.....__")
    await asyncio.sleep(5)
    await msg.edit("__Bot restarted !__")
    os.execv(sys.executable, ["python3", "-m", "mfinder"] + sys.argv)


@Client.on_message(filters.command(["logs"]) & filters.user(ADMINS))
async def log_file(bot, update):
    logs_msg = await update.reply("__Sending logs, please wait...__")
    try:
        await update.reply_document("logs.txt")
    except Exception as e:
        await update.reply(str(e))
    await logs_msg.delete()


@Client.on_message(filters.command(["server"]) & filters.user(ADMINS))
async def server_stats(bot, update):
    sts = await update.reply_text("__Calculating, please wait...__")
    total, used, free = shutil.disk_usage(".")
    ram = virtual_memory()
    start_t = time.time()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000

    ping = f"{time_taken_s:.3f} ms"
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    t_ram = humanbytes(ram.total)
    u_ram = humanbytes(ram.used)
    f_ram = humanbytes(ram.available)
    cpu_usage = cpu_percent()
    ram_usage = virtual_memory().percent
    used_disk = disk_usage("/").percent
    db_size = get_db_size()

    stats_msg = f"--**BOT STATS**--\n`Ping: {ping}`\n\n--**SERVER DETAILS**--\n`Disk Total/Used/Free: {total}/{used}/{free}\nDisk usage: {used_disk}%\nRAM Total/Used/Free: {t_ram}/{u_ram}/{f_ram}\nRAM Usage: {ram_usage}%\nCPU Usage: {cpu_usage}%`\n\n--**DATABASE DETAILS**--\n`Size: {db_size} MB`"
    try:
        await sts.edit(stats_msg)
    except Exception as e:
        await update.reply_text(str(e))
