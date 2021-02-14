# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 18:35:54 2021

@author: laura
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')


def index():
    return render_template('index.html',current_title='My Task Manager')


if __name__ == '__main__':
    app.run(debug=True)