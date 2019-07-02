from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    # Below makes parser belong to the Item class 
    # not an individual method
        
    # making sure that only some elements can be passed in
    # through the json payload
    # e.g. we should not be able to change the item name
    # setting up parser
    parser = reqparse.RequestParser()
    # parsing will look in json payload, but also form payloads
    # defining arguements
    parser.add_argument(
        'price',
        type=float,
        required=True, #no request can come through without price
        help="This field cannot be blank"
    )
    # Store id must be passed in whenever an ItemModel is created
    parser.add_argument(
        'store_id',
        type=int,
        required=True, #no request can come through without price
        help="Every item requires a store id"
    )

    @jwt_required()  # So we have to authenticate before calling GET method
    def get(self, name):
        # Below will return an object, so can't just return item
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}

    # Create
    def post(self, name):
        # Checking if item already exists
        if ItemModel.find_by_name(name):
            return {
               "message": "Item with name '{0}' already exists".format(name)
        }, 400 
        
        data = Item.parser.parse_args()
        
        # item = ItemModel(name, data['price'], data['store_id'])
        # Simplicifying the above below
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message': "An error occured inserting the item"}, 500

        return item.json(), 201
 
    # Update
    def put(self, name):  # idempotence action
        # only the vaild values from the payload will be put in 'data' variable
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
 
        if item is None:
            # Create new item
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            # Update existing item
            item.price = data['price']
            item.price = data['store_id']

        item.save_to_db()

        return item.json()

    # Delete
    def delete(self, name):
        # First find item by name
        item = ItemModel.find_by_name(name)

        if item:
            Item.delete_from_db()
        
        return {'message': 'Item \'{0}\' deleted'.format(name)}


class ItemsList(Resource):
    # Read
    def get(self):
        """
        Same result achieved wiht lambda and list comprehension
        return {
            'items': list(map(lambda x: x.json(), ItemModel.query.all()))
        } 
        """
        return {'items': [item.json() for item in ItemModel.query.all()]}
