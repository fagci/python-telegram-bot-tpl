#!/usr/bin/env python3

from pyrogram import Client, filters
from pyrogram.types import Message

from models import BotUser

ADMIN_ID = 202242124

client = Client('session')


def track(fn):
    async def ret(c, m):
        await fn(c, m, BotUser.from_user(m.from_user))
    return ret


@client.on_message(filters.command(['start', 'help']))
@track
async def help(_: Client, m: Message, u):
    await m.reply(f'Wellcome, {u}')


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
