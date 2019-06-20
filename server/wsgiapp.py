import sys
try: # called as __main__.py
    from server.servers import WSGI
    from server.endpoints import ENDPOINTS
except ImportError as init:
    try: # called as __init__.py
        from app.server.servers import WSGI
        from app.server.endpoints import ENDPOINTS
    except ImportError as problem:
        sys.exit(problem)

app = WSGI()

@app.route('/')
def index(req, res):
    return ENDPOINTS['/']().encode('UTF-8')

@app.route('/timestamp')
def timestamp(req, res):
    return '/' + ENDPOINTS.get(req.path, str)().encode('UTF-8')

@app.route('/undefined')
def api(req, res):
    print(req.path)
    return '/' + ENDPOINTS.get(req.path, str)().encode('UTF-8') 
