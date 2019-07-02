from flask_sqlalchemy import SQLAlchemy

# Have a SQLAlchemy object, which will look at the objects we
# tell it to, in our flask app. It will then map those objects
# to rows in a database.
# Putting a ItemMethod object into a db 
db = SQLAlchemy()


