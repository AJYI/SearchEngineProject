## https://flask.palletsprojects.com/en/1.1.x/quickstart/
# to run : export FLASK_APP=flask_try.py
# flask run

# import the Flask class from the flask module
from flask import Flask, render_template
from flask_pymongo import PyMongo

# create the application object
app = Flask(__name__)

# create to connect local mongodb
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('welcome.html')  # render a template

# @app.route('/serach<text>')
# def serach(text):
#     continue 



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)