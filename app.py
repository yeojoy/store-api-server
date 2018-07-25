from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # turn off auto tracking???
app.secret_key = 'second_server' # for JWT
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # endpoint is /auth

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/5000/item/yeojoy
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__': # if launch with python, this is the main!
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)