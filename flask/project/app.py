# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 18:35:54 2021

@author: laura
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return 'Bonjour le monde'


if __name__ == '__main__':
    app.run(debug=True)