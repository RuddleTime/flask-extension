from flask_restful import Resource

from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            # This will also return the items
            return store.json(), 200  # 200 is default
        # message gets returned in the body; 404 returned in status code
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
               "message": "Store with name '{0}' already exists".format(name)
        }, 400
        
        store = StoreModel(name)
        
        try:
            store.save_to_db()
        except:
            return {'message': "An error occured inserting the store"}, 500

        return store.json(), 201
 
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {'message': 'Store \'{0}\' deleted'.format(name)}


class StoresList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
