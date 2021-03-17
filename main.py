import vk_api
from flask import Flask, request, jsonify, send_file, send_from_directory
import json
from telethon import TelegramClient, sync
import sqlite3 as sql
import contextlib
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetHistoryRequest
import random

main = Flask(__name__, static_folder="pic")
#sio = socketio.Server()

a = []


def execute_statement(statement):
    with contextlib.closing(sql.connect('DB/data.db')) as conn:  # auto-closes
        with conn:  # auto-commits
            with contextlib.closing(conn.cursor()) as cursor:  # auto-closes
                cursor.execute(statement)
                values = cursor.fetchall()
                return values


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


@main.route('/reg', methods=['GET', 'POST'])
def handle_request2():
    log = request.form.get('log')
    pas = request.form.get('pass')
    sqlite_insert_query = f"INSERT INTO users (log, pass) SELECT '{log}', '{pas}' WHERE NOT EXISTS(SELECT 1 FROM users WHERE log = '{log}' AND pass = '{pas}');"
    execute_statement(sqlite_insert_query)
    return "zaebis"


@main.route('/', methods=['GET', 'POST'])
def handle_request1():
    sqlite_select_query = """SELECT * from users"""
    records = execute_statement(sqlite_select_query)
    log = request.form.get('log')
    pas = request.form.get('pass')
    print(log, pas)
    bd_log = 'standart'
    bd_pas = 'stand'
    tglog = request.form.get('tglog')
    print(tglog)
    for record in records:
        bd_log = record[1];
        bd_pas = record[2];
        if log == bd_log and pas == bd_pas:
            #socket.emit("status-update", "fsfsfsfsfsfsf")
            return "zaebis"
    return "hrenota"


@main.route('/zap', methods=['GET', 'POST'])
def handle_request3():
    con = sql.connect('DB/data.db')
    log = request.form.get('log')
    pas = request.form.get('pass')
    with con:
        cur = con.cursor()
        sqlite_insert_query = f"INSERT INTO users (log, pass) SELECT '{log}', '{pas}' WHERE NOT EXISTS(SELECT 1 FROM users WHERE log = '{log}' AND pass = 'pas');"
        cur.execute(sqlite_insert_query)
        con.commit()
    return "zaebis"


@main.route('/tgco', methods=['GET', 'POST'])
def handle_request11():
    vklog = request.form.get('tglog')
    vkpas = request.form.get('tgco')
    log = request.form.get('log')
    print(vklog, vkpas, log)

    api_id = 3070588
    api_hash = 'd672e46b2442ba3d680075bed9788121'
    number = request.form.get('tglog')
    client = TelegramClient(vklog, api_id, api_hash)
    
    client.connect()
    client.send_code_request(vklog)
    if vkpas !="0":
        client.sign_in(vklog, vkpas)
        sessia = StringSession.save(client.session)
        query = f"UPDATE users SET tglog = '{sessia}' WHERE log = '{log}';"
        print(sessia)
        execute_statement(query)
    return "zaebis"


@main.route('/vk', methods=['GET', 'POST'])
def handle_request12():
    vklog = request.form.get('tglog')
    vkpas = request.form.get('tgco')
    log = request.form.get('log')
    query = f"UPDATE users SET vklog = '{vklog}', vkpass = '{vkpas}' WHERE log = '{log}';"
    execute_statement(query)
    query = "SELECT * FROM users"
    print(execute_statement(query))
    return "zaebis"


@main.route('/jason', methods=['GET', 'POST'])
def handle_request10():
    data = {}
    log = request.form.get('log')
    pas1 = request.form.get('pass')
    quer = f"SELECT * FROM users WHERE log = '{log}' AND pass = '{pas1}'"
    sheets = execute_statement(quer)
    print("Здесь строки")
    print(sheets)
    number = "zero"
    co = "zero"
    for sheet in sheets:
        number = sheet[4]
        co = sheet[5]

    nextf = request.form.get('next')
    print(number, co)
    vk_session = vk_api.VkApi(number, co)
    vk_session.auth()
    vk = vk_session.get_api()
    posts = vk.newsfeed.get(start_from=nextf, count=3)
    post = posts['items']
    i = 0
    for post4 in post:
        if 'text' in post4 or 'attachments' in post4:
            if 'attachments' in post4 and 'text' in post4:
                #print(post4)
                posta = post4['attachments']
                photo = posta[0]
                if 'photo' in photo and 'text' in post4:
                    i = i + 1
                    sizes = photo['photo']
                    sizes1 = sizes['sizes']
                    size4 = sizes1[4]
                    data['message' + str(i)] = []
                    data['message' + str(i)].append({
                        'id': post4['text'],
                        'photo.id': size4['url'],
                        'text': 'vk'
                    })
                    continue
            if 'attachments' in post4:
                #print(post4)
                posta = post4['attachments']
                photo = posta[0]
                if 'photo' in photo and 'text' in post4:
                    i = i + 1
                    sizes = photo['photo']
                    sizes1 = sizes['sizes']
                    size4 = sizes1[4]
                    data['message' + str(i)] = []
                    data['message' + str(i)].append({
                        'id': 'a',
                        'photo.id': size4['url'],
                        'text': 'vk'
                    })
                    continue
            if 'text' in post4:
                if post4['text'] == '':
                    continue
                i = i + 1
                data['message' + str(i)] = []
                data['message' + str(i)].append({
                    'id': post4['text'],
                    'photo.id': "0",
                    'text': 'vk'
                })
    data['next'] = []
    data['next'].append({
        'nex': posts['next_from']
    })
    data['count'] = []
    data['count'].append({
        'count': i
    })
    # data = {
    #     "president": {
    #         "name": "Zaphod Beeblebrox",
    #         "species": "Betelgeusian"
    #     }
    # }
    # client.log_out()
    with open("data_file.json", "w+") as write_file:
        json.dump(data, write_file)
    print(data)
    return jsonify(data)


@main.route('/get_image')
def get_image():
    type = request.args.get('type')
    return a[int(type)]


@main.route('/tgposts', methods=['GET', 'POST'])
def handle_request5():
    api_id = 3070588
    api_hash = 'd672e46b2442ba3d680075bed9788121'
    log = request.form.get('log')
    pas1 = request.form.get('pass')
    print(log, pas1)
    quer = f"SELECT * FROM users WHERE log = '{log}' AND pass = '{pas1}'"
    sheets = execute_statement(quer)
    # str1 = sheets[4]
    # for sheet in sheets:
    #     str1 = sheet[3]
    # print(str1)
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
                        if i >= 1:
                            pora = True
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
    return jsonify(data)


import os

ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get("PORT", 17995))  # as per OP comments default is 17995
else:
    port = 3000

if __name__ == '__main__':
    main.run()
