import hashlib
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
    type = str,
    required = True,
    help = 'This field cannot be blank.'
)

_user_parser.add_argument('password',
    type = str,
    required = True,
    help = 'This field cannot be blank.'
)

class UserRegister(Resource):

    def post(self):
        
        data = _user_parser.parse_args()

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
    @jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        
        user.delete_from_db()

        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        
        # find user in database
        user = UserModel.find_by_username(data['username'])

        # This is what the 'authenticate()' function used to do
        # check password
        if user and safe_str_cmp(user.password, data['password']):
            # identity = is what the 'identity()' function used to do
            access_token = create_access_token(identity = user.id, fresh = True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401
        # create access token
        # create refresh token (we will look at this later)
        # return them