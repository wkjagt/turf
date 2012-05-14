from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import plugin_mount


class WebServer(HTTPServer):

    _arguments = {}

    def __init__(self, *args, **kwargs): 
        HTTPServer.__init__(self, *args, **kwargs)

    def set_argument(self, name, value):
        self._arguments[name] = value


    def get_argument(self, name):
        return self._arguments[name] if name in self._arguments else None




class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        path, query = self.parse_path()
        
        if path == '/favicon.ico':
            return
        
        event_type = 'registration'

        plugin = self.server.get_argument('plugin_container').get(event_type)

        results = plugin.get_results(query)
        


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

    # def get_event_type(self)


if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    try:
        web_server = WebServer((HOST, PORT), WebRequestHandler)
        web_server.set_argument('test', '23')


        # import pdb
        # from pprint import pprint as pp
        # pdb.set_trace()


        web_server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        web_server.socket.close()

