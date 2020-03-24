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
from NofarFinalProject.Models.Forms import ExpandForm
from NofarFinalProject.Models.Forms import CollapseForm

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




@app.route('/DATA' , methods = ['GET' , 'POST'])
def data():
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\accdatwebsite.csv'),encoding="utf-8")
    raw_data_table = ''
 
    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''
 
 
    return render_template(
    	'DATA.html',
        title='DATA',
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
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )





@app.route('/DataQuery', methods=['GET', 'POST'])
def DataQuery():

    Name = None
    HODESH_TEUNA = ''
    capital = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\accdatwebsite.csv'))
    df = df.set_index('HODESH_TEUNA')

    raw_data_table = df.to_html(classes = 'table table-hover')

    form = QueryFormStructure(request.form)
     
    if (request.method == 'POST' ):
        name = form.name.data
        HODESH_TEUNA = name
        if (name in df.index):
            capital = df.loc[name,'Capital']
            raw_data_table = ""
        else:
            capital = name + ', no such HODES TEUNA'
        form.name.data = ''



    return render_template('DataQuery.html', 
            form = form, 
            name = capital, 
           HODESH_TEUNA = HODESH_TEUNA,
            raw_data_table = raw_data_table,
            title='DataQuery by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )