# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:39:17 2021

@author: laura
"""
from app import app
from flask import render_template

@app.route('/')
@app.route('/index')


def index():
    return render_template('index.html',current_title='My Task Manager')

@app.route('/about')
def about():
    return render_template('about.html')
