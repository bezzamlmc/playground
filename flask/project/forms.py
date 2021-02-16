# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:49:11 2021

@author: laura
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('submit')