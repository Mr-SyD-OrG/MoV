# Do not edit this file, copy this file & rename it to const.py. Any format error will result in not getting start or help message.

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#use the same format for name & user_id placeholders
STARTMSG = """
Hɪ **[{}](tg://user?id={})** 🥶, I ᴀᴍ ᴀ ᴍᴇᴅɪᴀ ꜰɪɴᴅᴇʀ ʙᴏᴛ ᴡʜɪᴄʜ ꜱᴇᴀʀᴄʜ ꜰᴏʀ ꜰɪʟᴇꜱ ɪɴ ᴛᴇʟᴇɢʀᴀᴍ 😇. Jᴜꜱᴛ ꜱᴇɴᴅ qᴜᴇʀʏ ᴛᴏ ꜰɪɴᴅ ᴛʜᴇ ᴍᴇᴅɪᴀ. 🎐
Sᴇɴᴅ /help ꜰᴏʀ ᴍᴏʀᴇ ⚡."""

HELPMSG = """
**Yᴏᴜ ᴄᴀɴ ꜰɪɴᴅ ᴛʜᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ʜᴇʀᴇ.**
**Uꜱᴇʀ Cᴏᴍᴍᴀɴᴅꜱ:-**
/help - __Sʜᴏᴡ ᴛʜɪꜱ ʜᴇʟᴩ ᴍᴇꜱꜱᴀɢᴇ__
/settings - __Toggle settings of Precise Mode and Button Mode__
`Pʀᴇᴄɪꜱᴇ Mᴏᴅᴇ:` 
- __Iꜰ Eɴᴀʙʟᴇᴅ, ʙᴏᴛ ᴡɪʟʟ ᴍᴀᴛᴄʜ ᴛʜᴇ ᴡᴏʀᴅ 'ɴᴅ ʀᴇᴛᴜʀɴ ʀᴇꜱᴜʟᴛ ᴡɪᴛʜ ᴏɴʟʏ ᴛʜᴇ ᴇxᴀᴄᴛ ᴍᴀᴛᴄʜ__
- __Iꜰ Dɪꜱᴀʙʟᴇᴅ, ʙᴏᴛ ᴡɪʟʟ ᴍᴀᴛᴄʜ ᴛʜᴇ ᴡᴏʀᴅ 'ɴᴅ ʀᴇᴛᴜʀɴ ʀᴇꜱᴜʟᴛ ᴡɪᴛʜ ᴏɴʟʏ ᴛʜᴇ ᴇxᴀᴄᴛ ᴍᴀᴛᴄʜ__
`Rᴇꜱᴜʟᴛ Mᴏᴅᴇ:` 
- __Iꜰ Bᴜᴛᴛᴏɴ, ʙᴏᴛ ᴡɪʟʟ ʀᴇᴛᴜʀɴ ʀᴇꜱᴜʟᴛꜱ ɪɴ ʙᴜᴛᴛᴏɴ ꜰᴏʀᴍᴀᴛ__
- __Iꜰ Lɪꜱᴛ, ʙᴏᴛ ᴡɪʟʟ ʀᴇᴛᴜʀɴ ʀᴇꜱᴜʟᴛꜱ ɪɴ ʟɪꜱᴛ ꜰᴏʀᴍᴀᴛ__
- __Iꜰ HʏᴩᴇʀLɪɴᴋ, ʙᴏᴛ ᴡɪʟʟ ʀᴇᴛᴜʀɴ ʀᴇꜱᴜʟᴛꜱ ɪɴ ʜʏᴩᴇʀʟɪɴᴋ ꜰᴏʀᴍᴀᴛ__"""


START_KB = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⚝ Hᴇʟᴩ ⚝", callback_data="help_cb"),
            InlineKeyboardButton(
                "✧ Sᴜᴩᴩᴏʀᴛ ✧", url="https://t.me/Mod_Moviez_X"
            ),
        ]
    ]
)

HELP_KB = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("☚ Bᴀᴄᴋ", callback_data="back_m"),
        ],
    ]
)
