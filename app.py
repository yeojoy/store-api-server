import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# from security import authenticate, identity as identity_func
from resources.user import (
    User, UserRegister, UserLogin, TokenRefresh
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///my_app.db') # second one is default value
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # turn off auto tracking???
app.secret_key = os.environ.get('SECRET_KEY') # for JWT_SECRET_KEY

api = Api(app)

# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWTManager(app) # not creating /auth endpoint

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # claim means user's level(?). He/She is admin or not.
    if identity == 1: # Instead of hard-coding, you should read from a config file or a database
        return {'is_admin': True}
    
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked.'
    }), 401


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

@app.route('/')
def hello(self):
    return {'message': "Hello, World!"}

if __name__ == '__main__': # if launch with python, this is the main!
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)