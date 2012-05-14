from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import plugin_mount

class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):


    	event_type = 'registration'

        for plugin in plugin_mount.EventHandler.plugins:
        	if plugin.event_type == event_type:
       			plugin = plugin()





        path, query = self.parse_path()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write("{'msg' : 'hey there little buddy!'}")
        return            



    def parse_path(self):
        parsed_path = urlparse(self.path)

        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        return path, query


if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    try:
        web_server = HTTPServer((HOST, PORT), WebRequestHandler)
        web_server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

