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

        user = UserModel(**data) # UserModel(data['username'], data['password'])
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