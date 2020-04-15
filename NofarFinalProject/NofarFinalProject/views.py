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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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
from NofarFinalProject.Models.Forms import YomLayla 


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
@app.route('/Register', methods=['GET', 'POST'])
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
        'Register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )



@app.route('/DATA')
def DATA():
    """Renders the about page."""
    return render_template(
        'DATA.html',
        title='Data Model',
        year=datetime.now().year,
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



@app.route('/YomLayla' , methods = ['GET' , 'POST'])
def yomlayla():

    form1 = YomLayla()
    chart = ''

   
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/accdatwebsite.csv'))


    if request.method == 'POST':
        yl = int(form1.yl.data)


        df = df[['HODESH_TEUNA','YOM_LAYLA','HUMRAT_TEUNA']]
        df = df.loc[(df['YOM_LAYLA'] == yl)]
        new_df = pd.DataFrame()
        hodesh_list = list(set(df['HODESH_TEUNA']))
        new_df['HODESH'] = hodesh_list
        sug_list = list(set(df['HUMRAT_TEUNA']))
        for sug in sug_list:
            df_tmp = df.loc[(df['HUMRAT_TEUNA'] == sug)]
            s = df_tmp.groupby('HODESH_TEUNA').size()
            for i in range(1,13):
                if not i in s.index:
                    s[i] = 0
            s = s.sort_index()
            l = list(s)
            new_df[str(sug)] = l
        new_df = new_df.set_index('HODESH')
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        new_df.plot(ax = ax , kind='bar',stacked=True)
        chart = plot_to_img(fig1)

    
    return render_template(
        'YomLayla.html',
        img_under_construction = '/static/imgs/under_construction.png',
        form1 = form1,
        chart = chart
    )





@app.route('/dataset1')
def dataset1():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\accdatwebsite.csv'))
    raw_data_table = df.sample(30).to_html(classes = 'table table-hover')

    return render_template(
        'dataset1.html',
        title='Data set',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='This page displays data that can be analyzed and help us understand - ARE THERE UFOs ??'
    )

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String