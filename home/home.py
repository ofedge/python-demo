from flask import Flask, request, render_template, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from models import *

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/')
def index():
    post = Post.query.order_by(func.random()).first()
    return render_template('index.html', post=post)


@app.route('/add', methods=['POST', 'GET'])
def add_user():
    user = User(request.args.get('username'), request.args.get('password'))
    db.session.add(user)
    db.session.commit()
    return "add success"


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(username=username, password=password).first()
    if user:
        session['loginUser'] = user
        return redirect(url_for('post'))
    flash('Illegal username or password')
    return redirect(url_for('signin'))


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        return render_template('post.html')
    user = session.get('loginUser')
    if not user:
        return redirect(url_for('signin'))
    content = request.form['content']
    post = Post(user.id, content, datetime.now())
    db.session.add(post)
    db.session.commit()
    flash('post successed')
    return redirect(url_for('post'))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
