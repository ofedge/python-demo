from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "success"


@app.route('/add', methods=['POST', 'GET'])
def add_user():
    user = User(request.args.get('username'), request.args.get('password'))
    db.session.add(user)
    db.session.commit()
    return "add success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
