import vk_api
import json
from http.server import BaseHTTPRequestHandler,HTTPServer

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.request.get()
        self.send_response(200)

serv = HTTPServer(('https://dpsarvar.herokuapp.com/',80),HttpProcessor)
serv.serve_forever()
vk_session = vk_api.VkApi('+375447022103', '6626816')
vk_session.auth()

vk = vk_session.get_api()

posts = vk.newsfeed.get()

#with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(posts, f, ensure_ascii=False, indent=4)