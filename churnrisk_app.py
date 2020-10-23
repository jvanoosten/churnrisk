import urllib3, requests, json
from requests.auth import HTTPBasicAuth
from pprint import pprint
import os
import argparse
import sys
import json
import logging

def get_options(argv):
    parser = argparse.ArgumentParser()
    # store the file name
    parser.add_argument('-b', action='store', help='Bearer Token', required=True)
    parser.add_argument('-u', action='store', help='Prediction URL', required=True)
    parser.add_argument('-p', action='store', help='Payload', required=True)
    parser.add_argument('-l', action='store', help='logging level', default='INFO')
    options = parser.parse_args(argv)
    return options

def main():
    options = get_options(sys.argv[1:])
    bearer_token = options.b
    url = options.u
    payload = json.loads(options.p)
    # set the logging level 
    loglevel = options.l
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify -l DEBUG or -l debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
       raise ValueError('Invalid log level: %s' % loglevel.upper())
    logging.basicConfig(level=numeric_level)

    logging.info("Predicting churn risk.")

# Example payload for AutoAi deployed model: 
# 
#  '{"input_data":[{"fields":["ID","AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","AGE","TAXID","CREDITCARD","DOB","ADDRESS_1","ADDRESS_2","CITY","STATE","ZIP","ZIP4","LONGITUDE","LATITUDE","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[[1,"Adult","F","M",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]}]}'
# 
# Example payload for notebook deployed model:
# 
# '{"input_data":[{"fields":["AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[["Adult","F","M",2,25000,"N",5000,50,500,50,3.45,3,10,1500.0,0.0]]}]}'


    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bearer_token}
    response = requests.post(url, json=payload, headers=header, verify=False)
    pprint(json.loads(response.text))

if __name__ == "__main__":
    main()
