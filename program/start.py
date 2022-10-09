import asyncio

from datetime import datetime
from sys import version_info
from time import time

from config import (
    BOT_PHOTO,
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    SUDO_USERS,
    BOT_TOKEN,
    DEV_PHOTO,
    DEV_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from driver.decorators import sudo_users_only
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dbpunish import is_gbanned_user
from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, MessageNotModified
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(command("/start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_PHOTO}",
        caption=f"""هݪاެ حيݪي 🤎. ** » {message.from_user.mention()} !**\

اެناެ بۅت اެغاني ، بدۅن مقدماެت ضيفني ࢪاެح اެعجبك 🤎.
""",
        reply_markup=InlineKeyboardMarkup(
            [

                [
                    InlineKeyboardButton("", callback_data="cbhowtouse")
                    ],
                [
                    InlineKeyboardButton("المطور", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "‹ قناة المطور › ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "‹ لبوت للمطور ›", url=f"https://t.me/rcrcu"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "اضـف البـوت لمجمـوعتـك ✅",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                    )
                ],
            ]
        ),
    )


@Client.on_message(command(["بوت", f"", f"", f"البوت"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/0c4352a3255a8ee09ce72.jpg",
        caption=f"""I ،  bot play music in groups  \nDeveloper : @rcrcu \nMe bot Music : @cncebot""",
        reply_markup=InlineKeyboardMarkup(
         [
            [
            ],
            [
                InlineKeyboardButton(
                    "Me bot Music", url=f"https://t.me/cncebot"
                ),
            ],
            [
            ]
         ]
     )
  )

@Client.on_message(command(["لمطور", "المطور"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{DEV_PHOTO}",
        caption=f"""◍  :  مطور السورس \n\n√""",
        reply_markup=InlineKeyboardMarkup(
         [
            [
            ],
            [
                InlineKeyboardButton(
                        DEV_NAME, url=f"https://t.me/{OWNER_NAME}"
                ),
            ],
            [
            ]
         ]
     )
  )

@Client.on_message(command(["جلب التوكن", f"لب_التوكن", "hadow"]) & filters.private & ~filters.edited)
@sudo_users_only
async def shadow(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("انتظر من فضلك...")
    BOT_TOKEN = time() - start
    await m_reply.edit_text(f"**تم جلب التوكن**\n`{BOT_TOKEN}`")

@Client.on_message(command(["/ping", f"بنك"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["فحص", f"/uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ **شكرا لإضافتي إلى المجموعة !**\n\n"
                "قم بترقيتي كمسؤول عن المجموعة لكي أتمكن من العمل بشكل صحيح\nولا تنسى كتابة `/انضم` لدعوة الحساب المساعد\nقم بكتابة`/تحديث` لتحديث قائمة المشرفين",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("‹ المطور ›", url=f"https://t.me/rcrcu"),
                            InlineKeyboardButton("‹ قناة المطور ›", url=f"https://t.me/{GROUP_SUPPORT}")
                        ],
                        [
                            InlineKeyboardButton(
                        ALIVE_NAME, url=f"https://t.me/{ass_uname}"),
                        ],
                        [
                            InlineKeyboardButton(
                        "♡اضـف الـبـوت لـمـجـمـوعـتـك♡",
                        url=f'https://t.me/{BOT_USERNAME}?startgroup=true'),
                        ],
                    ]
                )
            )


chat_watcher_group = 5

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"👮🏼 (> {suspect} <)\n\n**Gbanned** user detected, that user has been gbanned by sudo user and was blocked from this Chat !\n\n🚫 **Reason:** potential spammer and abuser."
        )

