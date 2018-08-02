from flask_restful import reqparse, Resource
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    # when bad request like mismatching type or blank, resolve this problem.
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store's id."
    )

    @jwt_required
    def get(self, name):
        # item = next(filter(lambda i: i['name'] == name, items), 'None')
        # return {'message': item}, 200 if item is not None else 404
        item = ItemModel.find_by_name(name)
        if item:
            return {'item': item.json()}
        
        return {"message": "item not found."}, 404

    @jwt_required
    def post(self, name):
        
        # for item in items:
        #     if item['name'] == name:
        #         print(name + ' already exists.')
        #         return {'message': 'It already exists.'}, 400
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        
        new_item = ItemModel(name, data['price'], data['store_id']) # {'name': name, 'price': data['price']}

        # items.append(new_item)
        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # Internal server error
        
        return {'item': new_item.json()}, 201

    @fresh_jwt_required
    def put(self, name):
        #data = request.get_json(silent=True)

        #for item in items:
        #    if item['name'] == name:
        #        if item['price'] == data['price']:
        #            return {'message': 'prices are same.'}, 202
        #        else:
        #            item['price'] = data['price']
        #            return {'message': 'updating is success.'}, 200
        #        
        #return {'message': 'item not found'}, 404

        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price']) #{'name': name, 'price': data['price']}

        if item is None:
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
            # try:
            #     updated_item.save_to_db()
            # except:
            #     return {"message": "An error occurred inserting the itme."}, 500
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            # try:
            #     updated_item.update()
            # except:
            #     return {"message": "An error occurred updating the itme."}, 500
            item.price = data['price']

        item.save_to_db()

        return {'item': item.json()}


    @jwt_required
    def delete(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         items.remove(item)
        #         return {'message': 'success'}, 200
        # 
        # return {'message': 'item not found'}, 404
        
        # global items # python thinks items is local variable. so add "global" keyword
        # items = list(filter(lambda x: x['name'] != name, items))

        # connection = sqlite3.connect("my_app.db")
        # cursor = connection.cursor()
        # 
        # query = "DELETE FROM items WHERE name = ?"
        # cursor.execute(query, (name, ))
        # 
        # connection.commit()
        # connection.close()
        # 
        # return {'message': 'Item deleted.'}
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "{} deleted successfully.".format(name)}

        return {'message': 'Item not found.'}, 400


class ItemList(Resource):
    @jwt_optional
    def get(self):
        # connection = sqlite3.connect('my_app.db')
        # cursor = connection.cursor()
        # 
        # query = "SELECT * from items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # 
        # connection.close()
        # 
        # return {'items': items}, 200
        # return {'items': [item.json() for item in ItemModel.query.all()] }
        user_id = get_jwt_identity()
        items = list(map(lambda x: x.json(), ItemModel.find_all()))
        if user_id:
            return {'items': items}, 200

        return {
            'items': list(map(lambda item: item['name'], items)),
            'message': 'More data available if you log in.'
        }, 200