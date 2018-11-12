class client_data():
    def __init__(self,conn,addr):
        self._conn = conn;
        self._addr = addr;

class client_manager():
	def __init__(self):
		self._client_list = {}
	def add_user(self,conn,addr):
		identifier = hash(conn)
		self._client_list[identifier] = client_data(conn,addr)
		return identifier
	def remove_user(self,identifier):
		del self._client_list[identifier]
	def get_user(self,identifier):
		return self._client_list[identifier]
	def __getitem__(self, position):
		return self.get_user(position)
	def __iter__(self):
		return iter(self._client_list.keys())