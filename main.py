import vk_api
from flask import Flask, request, jsonify, send_file, send_from_directory
import json
from telethon import TelegramClient, sync
import sqlite3 as sql

main = Flask(__name__,static_folder="pic")

#def gettgposts():



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
    with con:
        cur = con.cursor()
        sqlite_insert_query = "INSERT INTO users (log, pass) SELECT 'Alex', 'alex' WHERE NOT EXISTS(SELECT 1 FROM users WHERE log = 'Alex' AND pass = 'alex');"
        cur.execute(sqlite_insert_query)
        con.commit()
    return "zaebis"


@main.route('/jason', methods=['GET', 'POST'])
def handle_request10():
    data = {}
    data['messages'] = []
    data['messages'].append({
        'id': 'Scott',
        'photo.id': 'stackabuse.com',
        'text': 'Nebraska'
    })
    # data = {
    #     "president": {
    #         "name": "Zaphod Beeblebrox",
    #         "species": "Betelgeusian"
    #     }
    # }
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
    if request.args.get('type') == '1':
       filename = 'izo1.png'
    else:
       filename = 'izo1.png'
    return send_file(filename, mimetype='image/png')


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