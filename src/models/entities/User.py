from werkzeug.security import check_password_hash # generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, username, password, fullname="") -> None:
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password(self, hashed_password, password):
        if hashed_password == password:
            return True
        return False

# print(generate_password_hash('123456'))