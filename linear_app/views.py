#!/usr/bin/env python3

from flask import Flask, render_template, url_for,	 request
from sklearn.externals import joblib
from numpy import round

import os


app = Flask(__name__)
#Permet d'importer toutes les variables de configuration
app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from .models import Result
from .models import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        regressor = joblib.load("./linear_regression_model.pkl")
        yearsExperience = [[float(dict(request.form)["YearsExperience"])]]
        prediction = (regressor.predict(yearsExperience)/100)*100

        result = Result(
            YearsExperience = yearsExperience[0][0],
            Prediction = float(prediction)
        )

        db.session.add(result)
        db.session.commit()


    return render_template("prediction.html", prediction = int(prediction), YearsExperience = int(yearsExperience[0][0]))


