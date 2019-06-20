'''
The HTTPHandler class handles the response logic, which is extensible through
the methods.py module where new functions should be stored, and in the 
endpoints.py module where those functions should be associated with a url route.
'''
import http.server

try: # __main__.py called
    from server.endpoints import ENDPOINTS
except ImportError as init:
    try: # __init__.py called
        from app.server.endpoints import ENDPOINTS
    except ImportError as problem: 
        sys.exit(problem)


class HTTPHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        '''
        Gets the route and tries to find it in the ENDPOINTS dict.
        ENDPOINTS has an associated method for valid routes.
        That method is called here, along with population of header data.
        Sent as response to client.
        '''
        try:
            data = ENDPOINTS.get(self.path, '/')() # execute the get method
        except TypeError as favicon: pass
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(data.encode('UTF-8'))
