class client_data():
    def __init__(self,conn,addr,thread):
        self._conn = conn;
        self._addr = addr;
        self._thread = thread;