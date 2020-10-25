#Importing necessary packages
from flask import Flask, request, render_template
import subprocess

import urllib3, requests, json
from requests.auth import HTTPBasicAuth
from pprint import pprint
import os
import argparse
import sys
import json
import logging

import numpy as np
import sklearn.pipeline

# Application scoped dictionary used as a cache
# TODO - replace with a redis DB
cache = {}

#Initializing the FLASK API
app = Flask(__name__)

def getPredictions(predictions_url, payload):

    return predictions

#Defining the home page for the web service
@app.route('/')
def home():
    return render_template('index.html')

#Authenticate user/password and store the bearer token
#  The <CP4D_URL>/v1/preauth/validateAuth url is passed in
@app.route('/authenticate', methods = ['POST'])
def authenticate():
    url  = request.args['url']
    user = request.args['user']
    password = request.args['password']
    response = requests.get(url, auth=HTTPBasicAuth(user, password), verify=False)
    token = response.json()['accessToken']
    cache['bearer_token'] = token
    return token

#Get the churn risk predictions
#   The <CP4D_URL>/v4/deployments/<UID>/predictions url is passed in
@app.route('/predict',methods=['POST'])
#Defining the predict method get input from the html page and to predict using the trained model
def predict():
    try:
        url = request.args['url']
        payload = request.json
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + cache['bearer_token']}
        response = requests.post(url, json=payload, headers=header, verify=False)
        predictions = json.loads(response.text)
        return render_template('index.html', prediction_text=predictions)
    except:
        return render_template('index.html', prediction_text='Prediction Err !!!') 

def get_options(argv):
    parser = argparse.ArgumentParser()
    # store the file name
    parser.add_argument('-l', action='store', help='logging level', default='INFO')
    options = parser.parse_args(argv)
    return options

def main():
    options = get_options(sys.argv[1:])
    # set the logging level 
    loglevel = options.l
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify -l DEBUG or -l debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
       raise ValueError('Invalid log level: %s' % loglevel.upper())
    logging.basicConfig(level=numeric_level)

    app.run(host= '0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main()
