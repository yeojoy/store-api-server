import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from security import authenticate, identity as identity_func
from resources.user import User, UserRegister, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///my_app.db') # second one is default value
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # turn off auto tracking???
app.secret_key = os.environ.get('SECRET_KEY') # for JWT_SECRET_KEY

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) # not creating /auth endpoint

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

@app.route('/')
def hello(self):
    return {'message': "Hello, World!"}

if __name__ == '__main__': # if launch with python, this is the main!
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)