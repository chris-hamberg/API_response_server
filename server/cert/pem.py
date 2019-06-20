''' use this script to generate a cert.pem for SSL server '''
import os

cmd = ('openssl req -x509 -newkey rsa:4096'
       ' -keyout cert.key -out cert.key -days 365 -nodes')
os.system(cmd)
