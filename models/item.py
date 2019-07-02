from db import db

# This class is extending db.Model
# Telling SqlAlchemy entity that these classes are things that
# we will be saving and retrieving from a db
class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # This must match the store's id type
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # SQLAlchemy does join work for us
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        # Return json representation of model (i.e. a dict)
        return {
            'name': self.name,
            'price': self.price
        }

    @classmethod
    def find_by_name(cls, name):
        # SQLAlchemy will not just find a row,
        # but automatically convert to an object if possible

        # .query comes from db.Model, it is a query builder
        # Under the hood the following query is running:
        # SELECT * FROM items WHERE name=name;
        
        # To select only the first row:
        # return ItemModel.query.filter_by(name=name).first()

        # The below returns an ItemModel object has
        # name and price, since this is a class method
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # This method is saving a model to the db
        # SQLAlchemy can directly translate from object to row,
        # so just need to tell it to insert current object

        # The session is a collection of object we are going to
        # add to the db. Multiple objects can be added.
        db.session.add(self)
        db.session.commit()

        # No longer require seperate 'create_item' and 'update_item'
        # methods, as 'save_to_db' covers both functionalities 

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
