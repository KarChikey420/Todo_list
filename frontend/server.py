from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

server = HTTPServer(('127.0.0.1', 8000), MyHandler)
print("Frontend server running at http://127.0.0.1:8000")
server.serve_forever()
