import random
import os
import hashlib

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
        self._password = self.hash_pass(password)
        self._has_password = True
    def add_hashed_pass(self,password):
        self._password = password
        self._has_password = True
    def hash_pass(self,password):
        return hashlib.sha256((password+self._salt).encode('UTF-8')).hexdigest()
    def check_pass(self,test_password):
        return self._password == self.hash_pass(test_password)

class book_keeper():
    def __init__(self,archive_name='user_data.dat'):
        self._archive_name = archive_name
        self._archive_handle = open(archive_name,"r+")
    def seek_user(self,username):
        self._archive_handle.seek(0,0)
        for line in self._archive_handle:
            split_line = line.split('\t')
            line_username = split_line[0]
            if line_username == username:
                self._archive_handle.seek(0,0)
                return {'username':username,'salt':split_line[1],'pass':split_line[2][:-1]}
        return False
    def add_entry(self,username,salt,password):
        if self.seek_user(username):
            return False
        else:
            self._archive_handle.seek(0,2)
            self._archive_handle.write('{}\t{}\t{}\n'.format(username,salt,password))
            self._archive_handle.flush()
            return True
    def load_whole_dump(self):
        result = {}
        self._archive_handle.seek(0,0)
        for line in self._archive_handle:
            split_line = line.split('\t')
            username = split_line[0]
            salt = split_line[1]
            password = split_line[2][:-1]
            user = user_data(salt,username)
            user.add_hashed_pass(password)
            result[username] = user
        return result

class user_manager():
    def __init__(self,archive_name='user_data.dat'):
        self.keeper = book_keeper(archive_name)
        self._user_list = self.keeper.load_whole_dump()
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
            self.keeper.add_entry(login,self._user_list[login]._salt,self._user_list[login]._password)
    def validate_user(self,login,password):
        user = self._user_list[login]
        if user._has_password:
            return user.check_pass(password)
        else:
            raise Exception('No password is set to user')
    def __getitem__(self,item):
        return self._user_list[item]
    def user_exists(self,login):
        return login in self._user_list
