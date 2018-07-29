import hashlib
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'This field cannot be blank.'
    )

    parser.add_argument('password',
        type = str,
        required = True,
        help = 'This field cannot be blank.'
    )

    def post(self):
        
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        password = data['password']
        if len(password) < 64:
            password = hashlib.sha256(password.encode()).hexdigest().upper()

        user = UserModel(data['username'], password) # UserModel(data['username'], data['password'])
        user.save_to_db()
        # connection = sqlite3.connect('my_app.db')
        # cursor = connection.cursor()
        # 
        # query = "INSERT INTO users VALUES (NULL, ?, ?)" # "id" is auto increment, so set NULL.
        # cursor.execute(query, (data['username'], data['password']))
        # 
        # connection.commit()
        # connection.close()

        return {'message': 'User created successfully.'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': 'User not found.'}, 404

        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        
        user.delete_from_db()

        return {'message': 'User deleted.'}, 200