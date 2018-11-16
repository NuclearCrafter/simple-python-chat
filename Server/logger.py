import threading
class logger():
	def __init__(self):
		self._thread_lock = threading.Lock()
	def log(self,message):
		self._thread_lock.acquire()
		print(message)
		self._thread_lock.release()