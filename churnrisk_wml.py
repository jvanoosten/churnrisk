from ibm_watson_machine_learning import APIClient
from pprint import pprint
import os
import argparse
import sys
import json
import logging

# Use the IBM Cloud API key that has been exported before running the application
def getAPIClient(apikey):  
  wml_credentials = { "url": "https://us-south.ml.cloud.ibm.com", "apikey": apikey }
  # create the API client 
  client = APIClient(wml_credentials)
  return client

def setDeploymentSpaceID(client, space_name):
    # get the ID of the deployment space of interest and set as the default
    for space in client.spaces.get_details()['resources']:
        if space_name in space['entity']['name']:
            space_id = space['metadata']['id']
            msg = 'deployment space: ' + space_name + ' id: ' + str(space_id)
            logging.debug(msg)
            print('deployment space: ', space_name, ', id: ', space_id)
            client.set.default_space(space_id)

# get the ID of the deployment name of interest
def getDeploymentID(client, deployment_name):
    deployment_details = client.deployments.get_details()
    for deployment in deployment_details['resources']:
        if deployment_name in deployment['entity']['name']:
          deployment_id = deployment['metadata']['id']
          msg = 'deployment name: ' + deployment_name + ' id' + str(deployment_id)
          logging.debug(msg)
          return deployment_id

# retreive the scoring ID
def getScoringID(client, deployment_details):
    scoring_id = client.deployments.get_uid(deployment_details)
    msg = 'scoring id: ' +  str(scoring_id)
    return scoring_id

def get_options(argv):
    parser = argparse.ArgumentParser()
    # store the file name
    parser.add_argument('-a', action='store', help='API key', required=True)
    parser.add_argument('-s', action='store', help='space name', required=True)
    parser.add_argument('-d', action='store', help='deployment name', required=True)
    parser.add_argument('-p', action='store', help='payload', required=True)
    parser.add_argument('-l', action='store', help='logging level', default='INFO')
    options = parser.parse_args(argv)
    return options

def main():
    options = get_options(sys.argv[1:])
    apikey = options.a
    space_name = options.s
    deployment_name = options.d
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
    client = getAPIClient(apikey)
    # space_list = client.spaces.list()
    setDeploymentSpaceID(client, space_name)
    deployment_id = getDeploymentID(client, deployment_name)
    print('deployment id: ', deployment_id)
    deployment_details = client.deployments.get_details(deployment_id)
    print('deployment details: ', deployment_details)
    scoring_id = getScoringID(client, deployment_details)

# Example payload for AutoAi deployed model: 
# 
#  '{"input_data":[{"fields":["ID","AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","AGE","TAXID","CREDITCARD","DOB","ADDRESS_1","ADDRESS_2","CITY","STATE","ZIP","ZIP4","LONGITUDE","LATITUDE","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[[1,"Adult","F","M",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]}]}'
# 
# Example payload for notebook deployed model:
# 
# '{"input_data":[{"fields":["AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[["Adult","F","M",2,25000,"N",5000,50,500,50,3.45,3,10,1500.0,0.0]]}]}'

    print('payload: ', payload)
    predictions = client.deployments.score(scoring_id, payload)
    pprint(predictions)

if __name__ == "__main__":
    main()
