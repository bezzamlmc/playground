# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:43:31 2021

@author: laura
"""
from app import db
db.create_all()
from datetime import datetime
from models import Task

t = Task(title="xyz", date=datetime.utcnow())
t