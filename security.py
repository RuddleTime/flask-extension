from werkzeug.security import safe_str_cmp
from models.user import UserModel

# function to authenticate user
# i.e. given a username and password, select the correct user
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# identity function is unique to flask-JWT
# takes in a payload (contents of JWT token)
# used when an endpoint needs to be authenticated
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id) 
