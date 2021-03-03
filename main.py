import vk_api
from flask import Flask, request
import sqlite3 as sql

main = Flask(__name__)


@main.route('/reg', methods=['GET', 'POST'])
def handle_request():
    con = sql.connect('DB/data.db')
    with con:
        cur = con.cursor()
        log = request.form.get('log')
        pas = request.form.get('pass')
        sqlite_insert_query = "INSERT INTO users (log, pass) SELECT '{log}', '{pas}' WHERE NOT EXISTS(SELECT 1 FROM users WHERE log = '{log}' AND pass = '{pas}');"
        cur.execute(sqlite_insert_query)
        con.commit()
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