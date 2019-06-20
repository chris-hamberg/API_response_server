from server.servers import Basic, SelfSigned, FlaskServer, WSGI
from server.servers import SERVER, THREADS
import sys


def main():
    '''
    Selects a server implementation based on the configuration file settings,
    and runs that server until killed by the enter key.
    '''
    # Generalized access to the various server implementations.
    servers = {
        "Basic":        Basic,
        "SelfSigned":   SelfSigned,
        "FlaskServer":  FlaskServer,
        "WSGI":         WSGI
        }

    # select server implementation from configuration file.
    server = servers.get(SERVER, lambda: sys.exit(
            'Invalid server in configuration.'))

    if server is FlaskServer:
        app = server()
        app.run()
    
    elif server is WSGI:
        from server.wsgiapp import app
        print(f'{server} server running...')
        print('ctrl-c to kill the server.')
        try:
            app.run()
        except KeyboardInterrupt as exit:
            print(f'Shutting {server} down...')
            sys.exit(0)

    else: # basic Python server selected. 
        que = [server(index) for index in range(THREADS)]
        print(f'{server} server running...')
        input('press enter to kill the server.')
        print(f'Shutting {server} down...')
        for listener in que:
            listener.server.shutdown()


if __name__ == '__main__':
    main()
