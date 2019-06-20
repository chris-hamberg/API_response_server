import sys
try: # __main__.py called
    from server.methods import *
except ImportError as init:
    try: # __init__.py called
        from app.server.methods import *
    except ImportError as problem:
        sys.exit(problem)

ENDPOINTS = {
        '/'        :   timestamp,
        '/timestamp':   timestamp,
        '/undefined':   lambda: str(2**(1/2)),
        }
