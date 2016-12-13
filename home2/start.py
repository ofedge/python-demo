#!/usr/bin/python3
#-*- coding:utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/tmp')
def tmp():
    return render_template('template.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
