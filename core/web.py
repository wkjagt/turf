from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import plugin_mount, json


class WebServer(HTTPServer):
    """
    Extending the HTTPServer to add argument getter and setter. We need to do this so we can 
    add arguments that are accessible to the RequestHandler.
    """
    _arguments = {}

    def set_argument(self, name, value):
        """
        Add an argument to the list of arguments
        """
        self._arguments[name] = value


    def get_argument(self, name):
        """
        Get an argument from the list of arguments
        """
        return self._arguments[name] if name in self._arguments else None




class WebRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Handle GET request
        """

        path, query = self.parse_path()
        
        if path == '/favicon.ico':
            return
        
        event_type = 'registration'

        plugin = self.server.get_argument('plugin_container').get(event_type)

        results = plugin.get_results(query)
        


        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results, indent=4))
        return



    def parse_path(self):
        parsed_path = urlparse(self.path)

        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        return path, query
