import vk_api
from flask import Flask, request
from telethon import TelegramClient, sync
import sqlite3 as sql

main = Flask(__name__)

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


@main.route('/tgupdate', methods=['GET', 'POST'])
def handle_request4():
    con = sql.connect('DB/data.db')
    with con:
        cur = con.cursor()
        log = request.form.get('log')
        tglog = request.form.get('tglog')
        sqlite_insert_query = "UPDATE users SET tglog = '{tglog}' WHERE log = '{log}';"
        print(tglog)
        cur.execute(sqlite_insert_query)
        con.commit()
    return "zaebis"


@main.route('/tgposts', methods=['GET', 'POST'])
def handle_request5():
    con = sql.connect('DB/data.db')
    with con:
        cur = con.cursor()
        log = request.form.get('log')
        sqlite_select_query = """SELECT * from users WHERE log = '{log}'"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        bd_log = 'standart'
        bd_pas = 'stand'
        tglog='+375447022103'

        api_id = 3070588
        api_hash = 'd672e46b2442ba3d680075bed9788121'

        client = TelegramClient('dp_sarvar', api_id, api_hash)
        tgco = request.form.get('tgco')
        client.connect()
        if not client.is_user_authorized():
            if tgco != "0":
                client.send_code_request(tglog)
                me = client.sign_in(tglog, tgco)
                client.connect()
                for dialog in client.iter_dialogs():
                    print(dialog.title)
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