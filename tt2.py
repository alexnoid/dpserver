from telethon import TelegramClient, sync
import sqlite3 as sql
import contextlib
from telethon.sessions import StringSession

api_id = 3070588
api_hash = 'd672e46b2442ba3d680075bed9788121'
number = '+375447022103'

client = TelegramClient('dp_sarvar', api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(number)
    client.sign_in(number, input())
print(StringSession.save(client.session))
# ata = {}
# ata['t'] = []
# ata['t'].append({
#     'a': 'eq',
#     'b': 'ffsf'
# })
# print(ata['t'])
# print(type(ata['t']))
