import vk_api
from flask import Flask, request, jsonify, send_file, send_from_directory
import json
from telethon import TelegramClient, sync
import sqlite3 as sql
import contextlib
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
import random

def execute_statement(statement):
    with contextlib.closing(sql.connect('DB/data.db')) as conn:  # auto-closes
        with conn:  # auto-commits
            with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                cursor.execute(statement)
                values = cursor.fetchall()
                return values

quer = f"SELECT * FROM users WHERE log = 'Alex' AND pass = 'alex'"
sheets = execute_statement(quer)
print(sheets[0][3])
api_id = 3070588
api_hash = 'd672e46b2442ba3d680075bed9788121'
s = "1ApWapzMBu5xdaUSOtQE4QelakhjhiNRjYIlejyK4zoK6aJ8QDHdjVM1dObcDesAQSlAkQpPKmDjQnkmLxZcZ-NvxDPnPZ4Kx4EOpsqaqA4FhtICjZztzNd-lRkrXmJujDuWVZ28aVhOaP9vbO78Qwfu9M_w7YWEeBxZNB-SobxzRpfNa1CHJh_b-PJdZxN4a-cbnB8ry4A2m8l-tyFiFCmpWLsEyVjLA5_s6d2lYMZCXrVoVWQA0W8Rt5DPD7UG_FhdlOHYshjID5qRDTtQPAEQeYOq8jhz-vKYIb66GU_UNSW86_d3m8qS0gqmA6avJJlrekLAkUygU2pYEmWBRy9dEToxkamI="
client = TelegramClient(StringSession(s), api_id, api_hash)
client.connect()
data = {}
i = 0
pora = False
for dialog in client.iter_dialogs():
    if not pora:
        if not dialog.is_group and dialog.is_channel:
            channel_entity = client.get_entity(dialog)
            posts = client(GetHistoryRequest(
                peer=channel_entity,
                limit=1,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0))
            for message in posts.messages:
                if message.message != '':
                    if i >= 3:
                        pora = True
                        print(message)
                        break
                    else:
                        if random.randint(1, 3) == 3:
                            i = i + 1
                            print(i)
                            print(message.message)
                            data['message' + str(i)] = []
                            data['message' + str(i)].append({
                                'id': message.message,
                                'photo.id': "0",
                                'text': 'telega'
                            })
with open("data_file.json", "w+") as write_file:
    json.dump(data, write_file)
print(data)