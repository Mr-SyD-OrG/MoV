from pyrogram.types import ChatJoinRequest
from pyrogram import Client, filters, enums
from mfinder.db.join_req import JoinReqs
from mfinder.db.settings_sql import get_channel, fsub_true
join_db = JoinReqs


@Client.on_chat_join_request((filters.group | filters.channel))
async def auto_syd(client, message: ChatJoinRequest):
    AUTH_CHANNEL = await get_channel()
    if message.chat.id == AUTH_CHANNEL:
      syd_user_id = message.from_user.id
      await fsub_true(syd_user_id)
      await client.send_message(syd_user_id, "Gᴏᴛ! Pʟᴇᴀꜱᴇ ᴄᴏɴᴛɪɴᴜᴇ...")





#By @SyD_Xyz
#Join @Bot_Cracker
