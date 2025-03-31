
from pyrogram import Client, filters, enums

join_db = JoinReqs


@Client.on_chat_join_request((filters.group | filters.channel))
async def auto_approve(client, message: ChatJoinRequest):
    if message.chat.id == AUTH_CHANNEL:
      ap_user_id = message.from_user.id
      first_name = message.from_user.first_name
      username = message.from_user.username
      date = message.date
      await join_db().add_user(user_id=ap_user_id, first_name=first_name, username=username, date=date)
