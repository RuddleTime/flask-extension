import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


# User class (above) must not be the same as the resource we use to let users sign up
# Making this a 'Resource' so it can be added to the API using Flask RESTful
# This could also be done by creating a resource endpoint
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank"
    ) 
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank"
    ) 
    # This will be called when we post some data to the user register
    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        
        if UserModel.find_by_username(username):
            return {'message': "User already exists"}, 400

        # user = UserModel(data['username'], data['password'])
        # Instead of the above, simplifiying by passing in the below
        # and unpacking the data
        # Since a parser (above) is being used, we know username and 
        # password will alway be there
        user = UserModel(**data)
        user.save_to_db() 

        return {'message': 'User created successfully'}, 201


