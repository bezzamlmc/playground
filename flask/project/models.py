# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:30:50 2021

@author: laura
"""
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'{self.title} created on {self.date}'