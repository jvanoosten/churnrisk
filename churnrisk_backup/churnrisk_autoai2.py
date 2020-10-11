from ibm_watson_machine_learning import APIClient
from pprint import pprint
import os

# Use the IBM Cloud API key that has been exported before running the application
# export APIKEY=<key>
apikey = os.getenv('APIKEY')

wml_credentials = {
                   "url": "https://us-south.ml.cloud.ibm.com",
                   "apikey": apikey
                  }

# create the API client 
client = APIClient(wml_credentials)

# prin the list of Deployment Spaces 
space_list = client.spaces.list()

# get the ID of the deployment space of interest and set as the default
space_name = os.getenv('DEPLOYMENT_SPACE')
for space in client.spaces.get_details()['resources']:
    if space_name in space['entity']['name']:
        space_id = space['metadata']['id']
        print('deployment space: ', space_name, ', id: ', space_id)
        client.set.default_space(space_id)

# get the ID of the deployment name of interest
deployment_name = os.getenv('DEPLOYMENT_NAME')
deployment_details = client.deployments.get_details()
for deployment in deployment_details['resources']:
    if deployment_name in deployment['entity']['name']:
      deployment_id = deployment['metadata']['id']
      print('deployment id: ', deployment_id)

# get the deployment details
dep_details = client.deployments.get_details(deployment_id)
print('deployment details: ', dep_details)

# retrieve the scoring endpoint
scoring_endpoint = client.deployments.get_scoring_href(dep_details)
print('Scoring endpoint: ', scoring_endpoint)

# retreive the scoring ID
scoring_id = client.deployments.get_uid(dep_details)

# set the payload
payload = {"input_data":[{"fields":["ID","AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","AGE","TAXID","CREDITCARD","DOB","ADDRESS_1","ADDRESS_2","CITY","STATE","ZIP","ZIP4","LONGITUDE","LATITUDE","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[[1,"Adult","F","M",None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]}]}
predictions = client.deployments.score(scoring_id, payload)
pprint(predictions)
