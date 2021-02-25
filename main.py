import vk_api
import time
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)


@app.route('/time')
def doyouhavethetime():
    def generate():
        while True:
            yield "{}\n".format(datetime.now().isoformat())
            time.sleep(1)
    return Response(generate(), mimetype='text/plain')

import os
ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get("PORT", 17995))  # as per OP comments default is 17995
else:
    port = 3000

server = HTTPServer(('', port), HttpProcessor)
server.serve_forever()
#t = threading.Thread(target=serv.serve_forever(), daemon=True)
#t.start()
vk_session = vk_api.VkApi('+375447022103', '6626816')
vk_session.auth()

vk = vk_session.get_api()

posts = vk.newsfeed.get()

# with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(posts, f, ensure_ascii=False, indent=4)