'''
This module consists of four response server implementations.

    1) basic multithreaded Python HTTP server. Accepts http get requests.

    2) self signed ssl multithreaded Python HTTP server. Accepts https get 
       requests.

    3) Flask framework development server. Accepts http get requests.
       (in production this version would rely on something like Apache
        rather than the builtin server.)

    4) Single threaded WSGI.
    
ENDPOINTS is a dictionary consisiting of URL route keys, and method values 
defined (as functions) in the methods.py module. The socketservers, and the 
Flask server dynamically respond to extensions in these files. The WSGI 
requires route implementations for each extension in wsgiapp.py.
'''
#TODO decouple the ip and port in the ADDR variable so all servers have config
##### for ip and port data. WSGI, and Flask implementations are currently
##### hard coded to localhost and port 5000 literals.
################################################################################
import http.server, inspect, os, re, socket, ssl, sys, time
import threading
from wsgiref.simple_server import make_server
from wsgiref.headers import Headers
from urllib.parse import parse_qs

try: # __main__.py called
    from server.endpoints import ENDPOINTS
    from server.configuration import SERVER, ADDR, THREADS
    from parser import parse
    args = parse()
    SERVER  = args.server or SERVER
    THREADS = args.threads or THREADS
    address = (f'{args.addr}', args.port) 
    ADDR = address if bool(args.addr) and bool(args.port) else ADDR
except ImportError as init:
    try: # __init__.py called
        from app.server.endpoints import ENDPOINTS
        from app.server.configuration import ADDR
        SERVER = "Basic"
    except ImportError as problem: 
        sys.exit(problem)
try: # don't depend on flask to execute.
    from flask import Flask
except ModuleNotFoundError as FAIL:
    pass
else:
    FAIL = False


#NOTE: Referential source for multithreaded implementation details:
###### stackoverflow.com/questions/14088294/multithreaded-web-server-in-python

#NOTE: Referential source for SSL with socketserver:
###### gist.github.com/dergachev/7028596


if SERVER == 'FlaskServer' or SERVER == 'WSGI':
    pass
else:
    # Create the server socket.
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SOCKET.bind(ADDR)
    SOCKET.listen(5)
    # import the request handler
    try:
        from server.handler import HTTPHandler
    except ImportError as init:
        try:
            from app.server.handler import HTTPHandler
        except ImportError as problem:
            sys.exit(problem)
#NOTE: for the SelfSigned SSL implementation
if SERVER == 'SelfSigned':
    # establish secure layer
    SOCKET = ssl.wrap_socket(
             SOCKET, 
             certfile='./app/server/cert/cert.pem', 
             server_side=True,
             ssl_version=ssl.PROTOCOL_TLS
             ) 


class Basic(threading.Thread):
    '''
    A simple multithreaded http server.
    '''
    def __init__(self, index):
        #### multithread ####
        super().__init__()
        self.index = index
        self.daemon = True
        #####################
        self.server = http.server.HTTPServer(
                ADDR, 
                HTTPHandler,
                False
                )
        self.set_secure_layer()
        self.start()

    def __repr__(self):
        return str(self.__class__.__name__)
    
    def set_secure_layer(self):
        self.server.socket = SOCKET

    def run(self):
        self.server_bind = self.server_close = lambda self: None
        self.server.serve_forever()

       
class SelfSigned(Basic):
    '''
    A multithreaded https server extends the Basic class with SSL.

    The only difference really is that this implementation uses a wrapped
    ssl.wrap_socket object.

    The existence of this class is mostly in prototypical meta.

    The physical implement provides the unique __repr__ method.
    '''
    pass

if FAIL: # we didn't use the FlaskServer
    class FlaskServer: pass
else:
    class FlaskServer:
        '''
        Totally different implementation compared to the two above.
        This implementation uses the Flask Framework.
        Multithreading is not implemented yet.
        '''
        #TODO this architecture should probably be restructured analog to 
        ##### the WSGI architecture in this application.
        app = Flask(__name__)
        
        @app.route('/', methods=['GET'])
        def timestamp():
            return ENDPOINTS['/']()

        @app.route('/<route>', methods=['GET'])
        def api(route):
            data = ENDPOINTS.get('/' + route, str)() # execute get method
            return data
        
        def run(self):
            FlaskServer.app.run('localhost', 5000)

class WSGI:
    '''
    Totally different server implementation compared to the three others above.
    Based on the Python standard library.
    
    Referential Source: Modern Python Standard Library Cookbook, 
    Alessandro Molina, Packt Publishing, page 263
    '''
    def __init__(self):
        self.endpoints = list()
    
    def __call__(self, environ, res):

        request = Request(environ)

        for regex, action in self.endpoints:
            match = regex.fullmatch(request.path)
            if match:
                request.urlargs = match.groupdict()
                break

        response = Response()

        if inspect.isclass(action):
            action = action()

        response.send(res)
        return [action(request, response)]

    def route(self, path):
        def _route_decorator(f):
            self.endpoints.append((re.compile(path), f))
            return f
        return _route_decorator

    def run(self):
        server = make_server('localhost', 5000, self)
        server.serve_forever()

class Response:
    ''' Used by the WSGI implementation '''
    def __init__(self):
        self.status = '200 OK'
        self.headers = Headers([
            ('Content-Type', 'application/json')
            ])

    def send(self, res):
        res(self.status, self.headers.items())

class Request:
    ''' Used by the WSGI implementation '''
    def __init__(self, environ):
        self.environ = environ
        self.urlargs = dict()

    @property
    def path(self):
        return self.environ['PATH_INFO']

    @property
    def query(self):
        return parse_qs(self.environ['QUERY_STRING'])
