#!/usr/bin/python3
#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, session, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import logging, time, hashlib, re, random


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'home'
SECRET_KEY = 'thisisaveryverysecretkey'


app = Flask(__name__)
app.config.from_object(__name__)
mongo = PyMongo(app)
logging.basicConfig(level=logging.DEBUG)


def get_ip():
    ''' get visitor realip '''
    ra = request.remote_addr
    rip = request.headers.get('X-Real-IP', '')
    return ra if ra else rip;


def get_timestamp():
    return int(time.time()*1000)


def md5(s):
    ''' md5 encryption '''
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def check_string(val):
    return re.match('^[0-9a-zA-Z]{4,18}$', val)


@app.route('/', methods = ['GET'])
def index():
    logging.info('--> Visitor Real IP: ' + str(get_ip()))
    count = mongo.db.excerpt.count()
    skip = random.randint(0, count-1)
    cursor = mongo.db.excerpt.find({},{'_id':0}).skip(skip).limit(1)
    experts = [c for c in cursor]
    expert = experts[0] if experts else None
    return render_template('index.html', expert=expert, url='')


@app.route('/game', methods = ['GET'])
def game():
    return render_template('game.html', url='game')


@app.route('/signin', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if not username or not check_string(username):
        return jsonify({'rtcode':0, 'msg': 'Invalid username'})
    elif not password or not check_string(password):
        return jsonify({'rtcode':0, 'msg': 'Invalid password'})
    else:
        md5_password = md5(password)
        user = mongo.db.users.find_one({
            'username': username,
            'password': md5_password
        })
        if not user:
            return jsonify({'rtcode':0, 'msg': 'Can not find user'})
        else:
            session['user'] = {
                'username': user.get('username'),
                'registration_time': user.get('registration_time'),
                'last_login': user.get('last_login'),
                'login_ip': get_ip()
            }
            mongo.db.users.update({
                '_id': user.get('_id')
            }, {'$set':{
                'last_login': get_timestamp(),
                'login_ip': get_ip()
            }})
            return jsonify({'rtcode': 1, 'msg': 'succeed!', 'data': session.get('user')})


@app.route('/wellread', methods = ['GET'])
def wellread():
    aid = request.args.get('aid')
    if not aid:
        articles = mongo.db.wellread.find({},{'title': 1}).sort([('sort', 1)])
        entities = []
        for article in articles:
            entities.append({'id':str(article['_id']), 'title': article['title']})
        return render_template('article.html', entities = entities, url = 'wellread')
    else:
        article = mongo.db.wellread.find_one({'_id': ObjectId(aid)}, {'title': 1, 'summary': 1, 'content': 1, '_id': 0})
        return jsonify({'rtcode': 1, 'msg': 'succeed!', 'data': article})


@app.route('/artifact', methods = ['GET'])
def artifact():
    aid = request.args.get('aid')
    if not aid:
        articles = mongo.db.artifact.find({},{'title': 1}).sort([('sort', 1)])
        entities = []
        for article in articles:
            entities.append({'id':str(article['_id']), 'title': article['title']})
        return render_template('article.html', entities = entities, url = 'artifact')
    else:
        article = mongo.db.artifact.find_one({'_id': ObjectId(aid)}, {'title': 1, 'summary': 1, 'content': 1, '_id': 0})
        return jsonify({'rtcode': 1, 'msg': 'succeed!', 'data': article})


@app.route('/signout', methods=['GET'])
def signout():
    session['user'] = None
    return jsonify({'rtcode': 1, 'msg': 'succeed!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
