# https://pythonbasics.org/flask-mongodb/

from flask import Flask
from flask_mongoengine import MongoEngine
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField() 
    email = db.StringField()

if __name__ == "__main__":
    app.run(debug=True)