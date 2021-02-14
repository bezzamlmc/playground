# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 18:35:54 2021

@author: laura
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')


def index():
    return '<h1>Bonjour</h1> Le Monde!'


if __name__ == '__main__':
    app.run(debug=True)