import sqlite3
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80)) # 80 is limit of text length
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # self.id = _id # id is python keyword. must add prefix '_'
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect('my_app.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row is not None:
        #     user = cls(*row) # User(row[0], row[1], row[2])
        # else:
        #     user = None
        # 
        # connection.close()
        # return user
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_userid(cls, _id):
        # connection = sqlite3.connect('my_app.db')
        # cursor = connection.cursor()
        # 
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # 
        # if row is not None:
        #     user = cls(*row)
        # else:
        #     user = None
        # 
        # connection.close()
        # return user
        return cls.query.filter_by(id = _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()