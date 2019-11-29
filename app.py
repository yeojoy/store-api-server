import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from security import authenticate, identity as identity_func
from resources.user import (
    User, UserRegister, UserLogin, UserLogout, TokenRefresh
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST_USER_IDS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///my_app.db') # second one is default value
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # turn off auto tracking???
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = [
    'access', 
    'refresh'
] # allow blacklisting for access and refresh tockens
app.secret_key = os.environ.get('SECRET_KEY') # for JWT_SECRET_KEY

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) # not creating "/auth" endpoint

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # if return true, user is in blacklist, so server launchs revoked_token_callback function.
    return decrypted_token['jti'] in BLACKLIST_USER_IDS

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/chair
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(TokenRefresh, '/refresh')

@app.route('/')
def hello(self):
    return {'message': "Hello, World!"}

if __name__ == '__main__': # if launch with python, this is the main!
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)