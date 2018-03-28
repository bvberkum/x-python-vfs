from pyvfs.vfs import Storage
from pyvfs.utils import Server

srv = Server(Storage())
# run the server in foreground
# to run in background, use start()
srv.run()
