import vk_api
import os
import json
import urllib.parse as urlparse

from http.server import BaseHTTPRequestHandler,HTTPServer

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        imsi = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('param1', None)
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('zaebis'.encode())

        #self.wfile.write("hello !")


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