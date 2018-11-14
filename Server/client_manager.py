class client_data():
    def __init__(self,conn,addr,username='GUEST'):
        self._conn = conn;
        self._addr = addr;
        self._user = username;

class client_manager():
    def __init__(self,filename='client_data.dump'):
        self._client_list = {}
    def add_user(self,conn,addr):
        identifier = hash(conn)
        self._client_list[identifier] = client_data(conn,addr)
        return identifier
    def remove_user(self,identifier):
        del self._client_list[identifier]
    def get_user(self,identifier):
        return self._client_list[identifier]
    def terminate_all_connections(self):
        for identifier in self._client_list:
            self._client_list[identifier]._conn.close()
    def __getitem__(self, position):
        return self.get_user(position)
    def __iter__(self):
        return iter(self._client_list.keys())

