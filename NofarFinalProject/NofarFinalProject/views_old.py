"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from NofarFinalProject import app




from NofarFinalProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from NofarFinalProject.Models.QueryFormStructure import QueryFormStructure 
from NofarFinalProject.Models.QueryFormStructure import LoginFormStructure 
from NofarFinalProject.Models.QueryFormStructure import UserRegistrationFormStructure 
from MofarFinalProject.Models.Forms import ExpandForm
from MofarFinalProject.Models.Forms import CollapseForm

###from NofarFinalProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines()

@app.route('/')
@app.route('/main')
def home():
    """Renders the main page."""
    return render_template(
        'main.html',
        title='Nofar project',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Home Page',
        year=datetime.now().year,
        message='Contact us'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Nofar project',
        year=datetime.now().year,
        message='What is the relationship between the number of accidents and the hours they occur'
    )
@app.route('/month')
def month():
    """Renders the month page."""
    return render_template(
        'month.html',
        title='month',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/main')
def main():
    """Renders the main page."""
    return render_template(
        'main.html',
        title='month',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/DATA')
def DATA():
    """Renders the DATA page."""
    return render_template(
        'DATA.html',
        title='Data Modiel',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/data/trump' , methods = ['GET' , 'POST'])
def trump():
	"""Renders the about page."""
	form1 = ExpandForm()
	form2 = CollapseForm()
	df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\trump.csv'))
    raw_data_table = ''
 
	if request.method == 'POST':
    	if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
    	if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
 
	
 
return render_template(
    	'trump.html',
        title='Trump',
    	year=datetime.now().year,
        message='My Trump page.',
        img_trump = '/static/imgs/trump.jpg',
        img_obama = '/static/imgs/trump.jpg',
        img_bush = '/static/imgs/trump.jpg',
        img_clinton = '/static/imgs/trump.jpg',
        raw_data_table = raw_data_table,
    	form1 = form1,
    	form2 = form2
	)