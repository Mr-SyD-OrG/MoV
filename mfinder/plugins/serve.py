import re
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
    LinkPreviewOptions,
)
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import UserNotParticipant, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from mfinder.db.files_sql import (
    get_filter_results,
    get_file_details,
    get_precise_filter_results,
)
from mfinder.db.join_req import JoinReqs
join_db = JoinReqs
from mfinder.db.settings_sql import (
    get_search_settings,
    get_admin_settings,
    get_link,
    get_channel,
    is_fsub,
)
from mfinder.db.ban_sql import is_banned
from mfinder.db.filters_sql import is_filter
from mfinder import LOGGER, ADMINS

async def is_subscribed(bot, query):
    try:
        if await is_fsub(query.from_user.id):
            return True
        else:
            try:
                AUTH_CHANNEL = await get_channel()
                user_data = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
            except UserNotParticipant:
                return False
            except Exception as e:
                LOGGER.warning(e)
                return False
            else:
                if user_data.status != enums.ChatMemberStatus.BANNED:
                    return True
                return False
    except Exception as e:
        LOGGER.warning(e)
        return False



        
@Client.on_message(
    ~filters.regex(r"^\/") & filters.text & filters.incoming
)
async def filter_(bot, message):
    user_id = message.from_user.id

    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if await is_banned(user_id):
        await message.reply_text("You are banned. You can't use this bot.", quote=True)
        return
    admin_settings = await get_admin_settings()
    if admin_settings:
        if admin_settings.repair_mode:
            return

    fltr = await is_filter(message.text)
    if fltr:
        await message.reply_text(
            text=fltr.message,
            quote=True,
        )
        return

    if 2 < len(message.text) < 100:
        search = message.text
        page_no = 1
        me = bot.me
        username = me.username
        result, btn = await get_result(search, page_no, user_id, username)

        if result:
            if btn:
                syd = await message.reply_text(
                    f"{result}",
                    reply_markup=InlineKeyboardMarkup(btn),
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                    quote=True,
                )
            else:
                syd = await message.reply_text(
                    f"{result}",
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                    quote=True,
                )
        else:
            syd = await message.reply_text(
                text="Nᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ. ❕\nOʀ ʀᴇᴛʀʏ ᴡɪᴛʜ ᴛʜᴇ <u>ᴄᴏʀʀᴇᴄᴛ ꜱᴩᴇʟʟɪɴɢ</u>🤐",
                quote=True,
            )
        await asyncio.sleep(600)
        await syd.delete()


@Client.on_callback_query(filters.regex(r"^(nxt_pg|prev_pg) \d+ \d+ .+$"))
async def pages(bot, query):
    user_id = query.from_user.id
    org_user_id, page_no, search = query.data.split(maxsplit=3)[1:]
    org_user_id = int(org_user_id)
    page_no = int(page_no)
    me = bot.me
    username = me.username

    result, btn = await get_result(search, page_no, user_id, username)

    if result:
        try:
            if btn:
                await query.message.edit(
                    f"{result}",
                    reply_markup=InlineKeyboardMarkup(btn),
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                )
            else:
                await query.message.edit(
                    f"{result}",
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                )
        except MessageNotModified:
            pass
    else:
        await query.message.reply_text(
            text="Nᴏ ʀᴇꜱᴜʟᴛꜱ ꜰᴏᴜɴᴅ. ❕\nOʀ ʀᴇᴛʀʏ ᴡɪᴛʜ ᴛʜᴇ <u>ᴄᴏʀʀᴇᴄᴛ ꜱᴩᴇʟʟɪɴɢ</u>🤐",
            quote=True,
        )


async def get_result(search, page_no, user_id, username):
    search_settings = await get_search_settings(user_id)
    if search_settings:
        if search_settings.precise_mode:
            files, count = await get_precise_filter_results(query=search, page=page_no)
            precise_search = "Enabled"
        else:
            files, count = await get_filter_results(query=search, page=page_no)
            precise_search = "Disabled"
    else:
        files, count = await get_filter_results(query=search, page=page_no)
        precise_search = "Disabled"

    if search_settings:
        if search_settings.list_mode:
            list_mode = "ON"
        else:
            list_mode = "OFF"
    else:
        list_mode = "OFF"

    if search_settings:
        if search_settings.link_mode:
            link_mode = "ON"
        else:
            link_mode = "OFF"
    else:
        link_mode = "OFF"

    if list_mode == "ON" and link_mode == "OFF":
        search_md = "List Button"
    elif list_mode == "OFF" and link_mode == "ON":
        search_md = "HyperLink"
    else:
        search_md = "Button"

    if files:
        btn = []
        index = (page_no - 1) * 10
        crnt_pg = index // 10 + 1
        tot_pg = (count + 10 - 1) // 10
        btn_count = 0
        result = f"**Sᴇᴀʀᴄʜ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ** `{search}` ❕"
        page = page_no
        for file in files:
            if list_mode == "ON":
                index += 1
                btn_count += 1
                file_id = file.file_id
                sydname = file.file_name.rsplit(".", 1)
                sydname = re.sub(r"[._()\-]", " ", sydname[0]) + "." + sydname[1]
                filename = (
                    f"**{index}.** `[{get_size(file.file_size)}]` - `{sydname}`"
                )
                result += "\n" + filename

                btn_kb = InlineKeyboardButton(
                    text=f"{index}", callback_data=f"file {file_id}"
                )

                if btn_count == 1 or btn_count == 6:
                    btn.append([btn_kb])
                elif 6 > btn_count > 1:
                    btn[0].append(btn_kb)
                else:
                    btn[1].append(btn_kb)
                
            elif link_mode == "ON":
                index += 1
                btn_count += 1
                file_id = file.file_id
                sydname = file.file_name.rsplit(".", 1)
                sydname = re.sub(r"[._()\-]", " ", sydname[0]) + "." + sydname[1]
                filename = f"**{index}.** [{sydname}](https://t.me/{username}/?start={file_id}) - `[{get_size(file.file_size)}]`"
                result += "\n" + filename
            else:
                file_id = file.file_id
                sydname = file.file_name.rsplit(".", 1)
                sydname = re.sub(r"[._()\-]", " ", sydname[0]) + "." + sydname[1]
                filename = f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), sydname.split()))}"
                btn_kb = InlineKeyboardButton(
                    text=f"{filename}", callback_data=f"file {file_id}"
                )
                btn.append([btn_kb])

        nxt_kb = InlineKeyboardButton(
            text="Nᴇxᴛ ⇉",
            callback_data=f"nxt_pg {user_id} {page + 1} {search}",
        )
        prev_kb = InlineKeyboardButton(
            text="⇇ Pʀᴇᴠɪᴏᴜꜱ",
            callback_data=f"prev_pg {user_id} {page - 1} {search}",
        )

        kb = []
        if crnt_pg == 1 and tot_pg > 1:
            kb = [nxt_kb]
        elif crnt_pg > 1 and crnt_pg < tot_pg:
            kb = [prev_kb, nxt_kb]
        elif tot_pg > 1:
            kb = [prev_kb]

        if kb:
            btn.append(kb)

        if list_mode == "ON":
            result = (
                result
                + "\n"
                + "__Tᴀᴩ ᴏɴ ʙᴇʟᴏᴡ ᴄᴏʀʀᴇꜱᴩᴏɴᴅɪɴɢ ꜰɪʟᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.__"
            )
        elif link_mode == "ON":
            result = result + "\n" + " __Tᴀᴩ ᴏɴ ꜰɪʟᴇ ɴᴀᴍᴇ & ᴛʜᴇɴ ꜱᴛᴀʀᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.__"

        return result, btn

    return None, None


@Client.on_callback_query(filters.regex(r"^file (.+)$"))
async def get_files(bot, query):
    user_id = query.from_user.id
    force_sub = await get_channel()
    if force_sub:
        try:
            if not await is_subscribed(bot, update):
                link = await bot.create_chat_invite_link(int(force_sub), creates_join_request=True)
                await query.reply_text(
                    text="**Pʟᴇᴀꜱᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴩᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴜꜱɪɴɢ ʙᴏᴛ !** 😶‍🌫️",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("❃ Jᴏɪɴ Uᴩᴅᴀᴛᴇꜱ Cʜᴀɴɴᴇʟ ❃", url=link.invite_link)]]
                    ),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    quote=True,
                )
                return
        except Exception as e:
            LOGGER.warning(e)
            await bot.send_message(
                ADMINS,
                text="Something went wrong, please contact my support group",
                quote=True,
            )

    if isinstance(query, CallbackQuery):
        file_id = query.data.split()[1]
        await query.answer("Sᴇɴᴅɪɴɢ ꜰɪʟᴇ...", cache_time=60)
        cbq = True
    elif isinstance(query, Message):
        file_id = query.text.split()[1]
        cbq = False
    filedetails = await get_file_details(file_id)
    admin_settings = await get_admin_settings()
    for files in filedetails:
        f_caption = files.caption
        if admin_settings.custom_caption:
            f_caption = admin_settings.custom_caption
        elif f_caption is None:
            f_caption = f"{files.file_name}"

        f_caption = "`" + f_caption + "`"

        if admin_settings.caption_uname:
            f_caption = f_caption + "\n" + admin_settings.caption_uname

        try:
            if query.message.chat.type != enums.ChatType.PRIVATE:
                msg = await bot.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    parse_mode=ParseMode.MARKDOWN,
                )
                await query.answer("Fɪʟᴇ ʜᴀꜱ ʙᴇᴇɴ ꜰᴏʀᴡᴀʀᴅᴇᴅ!.. Cʜᴇᴄᴋ DM 🗜️", show_alert=True)
            else:
                if cbq:
                    msg = await query.message.reply_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption,
                        parse_mode=ParseMode.MARKDOWN,
                        quote=True,

                    )
                else:
                    msg = await query.reply_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption,
                        parse_mode=ParseMode.MARKDOWN,
                        quote=True,
                    )
        except UserIsBlocked:
            await query.answer('Uɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴍᴀʜɴ !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://telegram.me/movies_forage_bot?start={file_id}")
        except Exception as e:
            await query.answer(url=f"https://telegram.me/movies_forage_bot?start={file_id}")
            

        if admin_settings.auto_delete:
            delay_dur = admin_settings.auto_delete
            delay = delay_dur / 60 if delay_dur > 60 else delay_dur
            delay = round(delay, 2)
            minsec = str(delay) + " mins" if delay_dur > 60 else str(delay) + " secs"
            disc = await bot.send_message(
                user_id,
                f"**⚠ <u>WARNING</u> ⚠ : \n\nPʟᴇᴀꜱᴇ <u>ꜱᴀᴠᴇ ᴛʜᴇ ꜰɪʟᴇ ʙʏ ʀᴇꜰᴏʀᴡᴀʀᴅɪɴɢ ɪᴛ ᴛᴏ ᴍᴇ</u>, ᴏʀ ᴛᴏ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇ, ɪᴛ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {minsec}**",
            )
            await asyncio.sleep(delay_dur)
            await disc.delete()
            await msg.delete()
            await bot.send_message(user_id, "❕ Fɪʟᴇ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ❕ \n[ᴩʟᴇᴀꜱᴇ ꜱᴇᴀʀᴄʜ ᴀɢᴀɪɴ ꜰᴏʀ ɪᴛ ✨]")


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return f"{size:.2f} {units[i]}"
