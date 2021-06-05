# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:43:31 2021

@author: laura
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somethingunique'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datalmc.db'

db = SQLAlchemy(app)
db.create_all()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'{self.title} created on {self.date}'

t = Task(title="xyz", date=datetime.utcnow())
t
db.session.add(t)
db.session.commit()

t = Task("newxyz", date=datetime.utcnow())
db.session.add(t)
db.session.commit()

tasks = Task.query.all()
tasks