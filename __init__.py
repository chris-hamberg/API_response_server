import app.server.servers
from app.server.servers import Basic

app.server.servers.SERVER  = "Basic"
app.server.servers.THREADS = 1
app.server.servers.ADDR    = ("localhost", 5000)
