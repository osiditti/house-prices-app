#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 20:33:05 2017

@author: ditti
"""

# import modules
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from collections import OrderedDict
import math
import pandas as pd
from sklearn.externals import joblib

# import helper functions
from helpers import *

# configure application
app = Flask(__name__)
#app.config.from_object('app.default_settings')
app.config.from_envvar('APP_SETTINGS')

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# secret key
app.secret_key = "0PaÿÌwâÉ°Cõ£\ÈBä,"

@app.route("/", methods=["GET", "POST"])
def index():
    """ Homepage with input forms."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # get input from user and put it in a dict
        house = OrderedDict([
            ('LotArea', request.form.get("LotArea")),
            ('1stFlrSF', request.form.get("1stFlrSF")),
            ('YearBuilt', request.form.get("YearBuilt")),
            ('GrLivArea', request.form.get("GrLivArea")),
            ('YearRemodAdd', request.form.get("YearRemodAdd"))
        ])
        
        # set min value for YearRemodAdd and convert to int
        for key, value in house.items():
            house[key] = int(value)
        
        if house['YearRemodAdd'] < 1950:
                house['YearRemodAdd'] = 1950

        # transform into pandas dataframe
        input = pd.DataFrame(house, columns=house.keys(), index=[0])
        
        # load xgboost regressor model
        regressor = joblib.load("model.dat")
        
        # predict and save result
        pred_price = regressor.predict(input)
        # instantiate result
        session["result"] = 0
        session["result"] = math.ceil(pred_price[0])
        
        # redirect to result page
        return redirect(url_for("predict"))

    # else, if user reached via GET
    else:
        # return homepage
        return render_template("index.html")

@app.route("/predict")
def predict():
    """ Display predicted house price."""
    
    # display result
    return render_template("predict.html", result = usd(session["result"]))

@app.route("/about")
def about():
    """ About page."""
    
    # display result
    return render_template("about.html")
