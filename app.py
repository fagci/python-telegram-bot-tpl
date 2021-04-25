#!/usr/bin/env python3

from pyrogram import Client, filters
from pyrogram.types import Message

from models import BotUser, db_session

ADMIN_ID = 202242124

client = Client('session')


def track(fn):
    async def ret(c, m):
        with db_session:
            await fn(c, m, BotUser.from_user(m.from_user))
    return ret


@client.on_message(filters.command(['start']))
@track
async def help(_: Client, m: Message, u: BotUser):
    u.start()
    await m.reply(f'Welcome, {u}', parse_mode=None)


@client.on_message(filters.command(['stop']))
@track
async def help(_: Client, __: Message, u: BotUser):
    u.stop()


@client.on_message(filters.command('users') & filters.chat(ADMIN_ID))
@track
async def users(_: Client, m: Message, __):
    total = BotUser.count()
    last = BotUser.last_created()

    await m.reply((
        'Total: %s\n'
        'Last: %s %s %s'
    ) % (
        total,
        last.created_at.strftime('%d.%m.%Y'),
        last.full_name,
        last.mention,
    ), parse_mode=None)


client.run()
