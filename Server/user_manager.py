import random
import pickle
import os

def generate_salt(l):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(l):
        chars.append(random.choice(ALPHABET))
    return ''.join(chars)

class user_data():
    def __init__(self,salt,login):
        self._salt = salt
        self._login = login
        self._logged_in = False
        self._has_password = False
    def add_pass(self, password):
        self._password = password
        self._has_password = True

class user_manager():
    def __init__(self,filename='user_data.dump'):
        if os.path.isfile(filename):
            try:
                self.load_dump(filename)
            except:
                self._user_list = {}
        else:
            self._user_list = {}
    def add_user(self, login):
        salt = generate_salt(20)
        self._user_list[login] = user_data(salt,login)
        return salt
    def get_user_salt(self,login):
        if login in self._user_list:
            return self._user_list[login]._salt
    def set_user_password(self,login,password):
        if login in self._user_list:
            self._user_list[login].add_pass(password)
            self.dump()
    def validate_user(self,login,password):
        user = self._user_list[login]
        if user._has_password:
            if user._password == password:
                return True
            else:
                return False
        else:
            raise Exception('No password is set to user')
    def load_dump(self,filename='user_data.dump'):
        file = open(filename,'rb')
        self._user_list = pickle.load(file)
        file.close()
    def dump(self,filename='user_data.dump'):
        file = open(filename,'wb')
        pickle.dump(self._user_list,file)
        file.close()
    def __getitem__(self,item):
        return self._user_list[item]
    def user_exists(self,login):
        return login in self._user_list