import vk_api
import os
import json
from http.server import BaseHTTPRequestHandler,HTTPServer

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        #self.request.get()
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<html><head><title>Title goes here.</title>хуй пизда залупа</head>".encode())
        #self.wfile.write("hello !")

PORT = os.environ['PORT']
serv = HTTPServer(('',PORT),HttpProcessor)
serv.serve_forever()
vk_session = vk_api.VkApi('+375447022103', '6626816')
vk_session.auth()

vk = vk_session.get_api()

posts = vk.newsfeed.get()

#with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(posts, f, ensure_ascii=False, indent=4)