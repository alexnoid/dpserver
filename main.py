import vk_api
from PIL import Image
from flask import Flask, request, jsonify, send_file, send_from_directory
import json
from telethon import TelegramClient, sync
import sqlite3 as sql

main = Flask(__name__,static_folder="pic")

#def gettgposts():

a = []


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
    con = sql.connect('DB/data.db')
    with con:
        cur = con.cursor()
        log = request.form.get('log')
        pas = request.form.get('pass')
        sqlite_insert_query = "INSERT INTO users (log, pass) SELECT '{log}', '{pas}' WHERE NOT EXISTS(SELECT 1 FROM users WHERE log = '{log}' AND pass = '{pas}');"
        cur.execute(sqlite_insert_query)
        con.commit()
    return "zaebis"


@main.route('/', methods=['GET', 'POST'])
def handle_request1():
    con = sql.connect('DB/data.db')
    with con:
        cur = con.cursor()
        sqlite_select_query = """SELECT * from users"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
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
            return "zaebis"
    return "hrenota"


@main.route('/zap', methods=['GET', 'POST'])
def handle_request3():
    con = sql.connect('DB/data.db')
    log = request.form.get('log')
    pas = request.form.get('pass')
    with con:
        cur = con.cursor()
        sqlite_insert_query = "INSERT INTO users (log, pass) SELECT '{log}', '{pas}' WHERE NOT EXISTS(SELECT 1 FROM users WHERE log = 'Alex' AND pass = 'alex');"
        cur.execute(sqlite_insert_query)
        con.commit()
    return "zaebis"

@main.route('/tgco', methods=['GET', 'POST'])
def handle_request11():
    api_id = 3070588
    api_hash = 'd672e46b2442ba3d680075bed9788121'
    number = request.form.get('tglog')
    client = TelegramClient('dp_sarvar', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(number)
    client.log_out();
    return "zaebis"


@main.route('/jason', methods=['GET', 'POST'])
def handle_request10():
    # api_id = 3070588
    # api_hash = 'd672e46b2442ba3d680075bed9788121'
    # number = request.form.get('tglog')
    # co = request.form.get('tgco')
    # client = TelegramClient('dp_sarvar', api_id, api_hash)
    # client.connect()
    # client.send_code_request(number)
    # me = client.sign_in(number, co)
    # x = [[d.unread_count, d.title] for d in client.get_dialogs() if not getattr(d.entity, 'is_private', False) and d.unread_count != 0]
    # print(client.get_me().stringify())
    channel_username = 'portablik'

    data = {}
    # data['message1'].append({
    #     'id': 'Scott',
    #     'photo.id': 'https://dpsarvar.herokuapp.com/pic/izo1.png',
    #     'text': 'текст поста'
    # })
    i = 0
    # for message in client.iter_messages(channel_username, limit=10):
    #     data['message'+str(i)] = []
    #     data['message'+str(i)].append({
    #         'id': message.id,
    #         'photoid': '0',
    #         'text': str(message.text)
    #     })
    #     i+1

    number = request.form.get('tglog')
    co = request.form.get('tgco')

    vk_session = vk_api.VkApi(number, co)
    vk_session.auth()

    vk = vk_session.get_api()

    posts = vk.newsfeed.get()

    post = posts['items']
    i =0
    for post4 in post:
        i=i+1
        if 'attachments' in post4:
            data['message'+str(i)] = []
            print('Нет')
            posta = post4['attachments']
            photo = posta[0]
            sizes = photo['photo']
            sizes1 = sizes['sizes']
            size4 = sizes1[4]
            data['message'+str(i)].append({
                'id': post4['text'],
                'photo.id': size4['url'],
                'text': 'текст поста'
    })
            break

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


@main.route('/tgupdate', methods=['GET', 'POST'])
def handle_request4():
    try:
        con = sql.connect('DB/data.db')
        with con:
            cur = con.cursor()
            log = request.form.get('log')
            tglog = request.form.get('tglog')
            sqlite_insert_query = "UPDATE users SET tglog = '{tglog}' WHERE log = '{log}';"
            print(tglog)
            cur.execute(sqlite_insert_query)
            con.commit()
            cur.close()
    except sql.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sql.Connection):
            con.close()
            print("The SQLite connection is closed")
    return "zaebis"


@main.route('/get_image')
def get_image():
    type = request.args.get('type')
    return a[int(type)]


@main.route('/tgposts', methods=['GET', 'POST'])
def handle_request5():
    try:
        con = sql.connect('DB/data.db')
        with con:
            cur = con.cursor()
            log = request.form.get('log')
            sqlite_select_query = """SELECT * from users WHERE log = '{log}'"""
            rows = cur.execute(sqlite_select_query)
            tglogb = "no";
            for row in rows:
                tglogb = row[2];
            records = cur.fetchall()
            cur.close()
            bd_log = 'standart'
            bd_pas = 'stand'
            tglog='+375447022103'
            print(tglogb)

            api_id = 3070588
            api_hash = 'd672e46b2442ba3d680075bed9788121'

            client = TelegramClient('dp_sarvar', api_id, api_hash)
            tgco = request.form.get('tgco')
            client.connect()
            channel_username = 'vvalst'
            for message in client.iter_messages(channel_username, limit=100):
                if message.photo:
                    img = client.download_media(message.media, )
                    print(img)
    except sql.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sql.Connection):
            con.close()
            print("The SQLite connection is closed")
    return "zaebis"


import os
ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get("PORT", 17995))  # as per OP comments default is 17995
else:
    port = 3000


if __name__ == '__main__':
    main.run()

#vk_session = vk_api.VkApi('+375447022103', '6626816')
#vk_session.auth()

#vk = vk_session.get_api()

#posts = vk.newsfeed.get()

# with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(posts, f, ensure_ascii=False, indent=4)