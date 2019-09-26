from flask_restful import reqparse, Resource
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
)
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    # when bad request like mismatching type or blank, resolve this problem.
    parser.add_argument(
        'price', type = float, required = True, help = "This field cannot be left blank!"
    )

    parser.add_argument(
        'store_id', type = int, required = True, help = "Every item needs a store's id."
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {"message": "item not found."}, 404

    @fresh_jwt_required
    def post(self, name):
        
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400


        data = Item.parser.parse_args()
        
        new_item = ItemModel(name, **data)

        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # Internal server error
        
        return new_item.json(), 201

    @jwt_required
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item deleted."}, 200

        return {'message': 'Item not found.'}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        
        return {'items': list(map(lambda item: item['name'], items))}, 200