# Model Deployment with IBM Watson Studio and Watson Machine Learning.

How do you get value from AI models?   By deploying and infusing them into applications.


![AI Ladder](images/AILadder.png)

### Introduction

IBM Watson Studio and Watson Machine Learning are available on the IBM Cloud and those components are also integrated with the IBM Cloud Pak for Data (CP4D).   They can be used to develop AI models and deploy them.   This project outlines how to do this in the IBM Cloud but the process is also applicable to where ever you are running CP4D.

### Pre-requisites

- Open an [IBM Clound account](https://www.ibm.com/cloud) or sign-in.
- Add several services; Cloud Object Storage, Watson Studio, and Watson Machine Learning. 
- Create an API key. 

The services are available with Lite (free) options to help you get started.

![IBM Cloud services](images/IBM_Cloud_services.png)

The API key can be created by navigating the top menu `Manage -> Access (IAM)`

![API Key](images/APIKEY.png)

You can only see the key value at creation time.   Save the key value in a safe place.  We will use it when creating an APIClient.

### Project Setup

Start by cloning this project on your desktop and changing to the churnrisk directory.

`git clone https://github.com/jvanoosten/churnrisk.git`

`cd churnrisk`

Now go to the IBM Cloud and start at Resource List screen, select the Watson Studio service and push the `Get Started` button.

![Get Started](images/WatsonStudioGetStarted.png)

Use the Quick Navigation link to go to the `Deployment spaces` and select the option  For a name, specify `churnrisk_deployment_space`.  Select the cloud object storage and watson machine learning services that you want associated with the space.    

![Create space](images/create_deployment_space.png)
 
Use the Quick Navigation link in Watson Studio to go to the `Projects`.

Create a new empty project call `churnrisk` and select your cloud object storage to be used by the project. 

![Create project](images/new_project.png)

Projects include Assets like datasets and notebooks, Environments like notebook runtime environments with Python, Jobs that can be scheduled, Access Control for controling collaborator authorizatoins, and Settings.

Within the project `Settings`, create a new `Access token` called `churnrisk_access_token`.  This token will be used in a notebook to save files to the project.  

![New Token](images/churnrisk_access_token.png)


This token will be used in a notebook to save files to the project.  The value of the token can be viewed at anytime using the view option for the token.

![Token view](images/view_token.png)

Highlight the token to copy it. 

![Token view](images/token_value.png)

### Add the Dataset and Notebook Assets to the Project

You can add Assets to the project using blue `Add to project +` button at the top of the project.   We want to add the Within the projects `Assets`, 

![Add to project](images/add_to_project.png)

#### Add dataset

Add a dataset to the project by selecting the `Data` button.Add a dataset asset to your project.  You can use the browse button or drag and drop to upload the `customer_demochurn_activity_analyze.csv` included in the churnrisk github project.

#### Add notebook

Use the `Add to project` menu option and select the `Notebook` as the asset type.  Create the new notebook by using the `From file` option.  Drag and drop the `TradingCustomerChurnClassifier.ipynb` file to upload it. 

![New notebook](images/new_notebook.png)

Press complete to create the notebook.   An Python36 environment will be created and the notebook will be ready to execute.   

### Execute the notebook

The TradingCustomerChurnClassifier notebook 

![New notebook](images/TradingCustomerChurnClassifier.png)

The notebook 

1. Ingest merged customer demographics and trading activity data
2. Visualize merged dataset and get better understanding of data to build hypotheses for prediction
3. Leverage sklearn library to build classification model that predicts whether customer has propensity to churn
4. Expose the classification model as RESTful API endpoint for the end-to-end customer churn risk prediction and risk remediation application

You can execute the notebook cells using the widgets at the top of the page or by pressing `Shift-Enter`.

#### Load Data 

The code to load the dataset is inserted in the notebook by using the data wizard. 

![Insert code](images/notebook_pandas_dataframe_code_insert.png)

After insert:

![Insert code](images/notebook_pandas_dataframe_loaded.png)

#### Save the model to the deployment space

The model is deployed online by following these steps:

1. Lookup the pre-created deployment space.
2. Set this deployment space as the default space.
3. Store the model pipeline in the deployment space. Enter the name for the model in the cell below.
4. Deploy the saved model. Enter the deployment name in the cell below.
5. Retrieve the scoring endpoint to score the model with a payload

The ibm_watson_machine_learning library is used to complete these steps.

You need to insert your API key to create the APIClient. 

![Create APIClient](images/APIClient_create.png)

After the model is saved and deployed online, it can be scored (called to make predictions).

![Score model](images/score_model.png)

#### Useful helper functions 

A `create_download_link_csv` function is defined that can be used to create a download dataset button within the notebook. 

Examples are included showing how to save and restore the model using two different packages: joblib and pickle.

Finally, the project_lib package is used to save `churnrisk.pkl` to the project data assets.  The serialized model can be downloaded from the project to be used in application.  

![Save model to project](images/project_lib.png)

The project id can be found in the URL for the notebook.  The ID starts after `projectid=` and ends before the `&`.  The project id is `13f6e435-488e-4f71-97a0-3a4abd877587` in this example.

`https://dataplatform.cloud.ibm.com/analytics/notebooks/v2/87df1173-28a4-4040-80cb-ad1ad5832fb2?projectid=13f6e435-488e-4f71-97a0-3a4abd877587&context=cpdaas`

The Access Token was created earlier in Project Settings. 

### Execute the churnrisk applications on your workstation 

#### Execute the churnrisk_app.py 

The churnrisk_app.py uses a python request to make a REST api call to the deployed model.

The `python churnrisk_app.py -h` command show the help.  

```
usage: churnrisk_app.py [-h] -b B -u U -p P [-l L]

optional arguments:
  -h, --help  show this help message and exit
  -b B        Bearer Token
  -u U        Prediction URL
  -p P        Payload
  -l L        logging level
```
Note: The Bearer Token be obtained by running the auth.py 

usage: auth.py [-h] -a A -u U -p P [-l L]

optional arguments:
  -h, --help  show this help message and exit
  -a A        Auth URL
  -u U        User
  -p P        Password
  -l L        logging level
  
`python auth.py -a <CP4D_URL>/v1/preauth/validateAuth -u USER_ID -p PASSWORD`


The predictions url is the form `<CP4D_URL>/v4/deployments/<UID>/predictions` taken from from the churnrisk deployment in CP4D. 

Sample command:

`python churnrisk_app.py -b. BEARER_TOKEN -u PREDICTIONS_URL -p '{"input_data":[{"fields":["AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[["Adult","F","M",2,25000,"N",5000,50,500,50,3.45,3,10,1500.0,0.0]]}]}'`

Produces this output:

```
INFO:root:Predicting churn risk.
/Users/jimvo/opt/anaconda3/lib/python3.7/site-packages/urllib3/connectionpool.py:847: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
{'predictions': [{'fields': ['prediction', 'probability'],
                  'values': [[2, [0.12, 0.41, 0.47]]]}]}
```

The prediction is shown at the bottom of the output.


#### Execute the churnrisk_wml.py 

The churnrisk_wml.py uses the APIClient from the ibm_watson_machine_learning to call the deployed model similar to example in the notebook.

The `python churnrisk_wml.py -h` command show the help.  

```
usage: churnrisk_app.py [-h] -a A -s S -d D -p P [-l L]
churnrisk_app.py: error: the following arguments are required: -a, -s, -d, -p

Where:
  -a A        API key
  -s S        space name
  -d D        deployment name
  -p P        payload
  -l L        logging level (optional)
```

Sample command:

`python churnrisk_wml.py -a YOUR_API_KEY -s churnrisk_deployment_space -d churnrisk_model_deployment -p '{"input_data":[{"fields":["AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[["Adult","F","M",2,25000,"N",5000,50,500,50,3.45,3,10,1500.0,0.0]]}]}'`

Produces this output:

```
deployment space:  churnrisk_deployment_space , id:  d39f197b-5193-40a5-aaec-c6cb34582740
deployment id:  e7946bcb-af93-440a-a465-b685d54681aa
deployment details:  {'entity': {'asset': {'id': 'b02304e3-2b21-448e-83f7-7f01f0554b34'}, 'custom': {}, 'deployed_asset_type': 'model', 'hardware_spec': {'id': 'Not_Applicable', 'name': 'S', 'num_nodes': 1}, 'name': 'churnrisk_model_deployment', 'online': {}, 'space_id': 'd39f197b-5193-40a5-aaec-c6cb34582740', 'status': {'online_url': {'url': 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e7946bcb-af93-440a-a465-b685d54681aa/predictions'}, 'state': 'ready'}}, 'metadata': {'created_at': '2020-10-11T14:48:21.895Z', 'id': 'e7946bcb-af93-440a-a465-b685d54681aa', 'modified_at': '2020-10-11T14:48:21.895Z', 'name': 'churnrisk_model_deployment', 'owner': 'IBMid-550008YAWT', 'space_id': 'd39f197b-5193-40a5-aaec-c6cb34582740'}}
payload:  {'input_data': [{'fields': ['AGE_GROUP', 'GENDER', 'STATUS', 'CHILDREN', 'ESTINCOME', 'HOMEOWNER', 'TOTALDOLLARVALUETRADED', 'TOTALUNITSTRADED', 'LARGESTSINGLETRANSACTION', 'SMALLESTSINGLETRANSACTION', 'PERCENTCHANGECALCULATION', 'DAYSSINCELASTLOGIN', 'DAYSSINCELASTTRADE', 'NETREALIZEDGAINS_YTD', 'NETREALIZEDLOSSES_YTD'], 'values': [['Adult', 'F', 'M', 2, 25000, 'N', 5000, 50, 500, 50, 3.45, 3, 10, 1500.0, 0.0]]}]}
{'predictions': [{'fields': ['prediction', 'probability'],
                  'values': [[2, [0.3, 0.3, 0.4]]]}]}
```
The prediction is shown at the bottom of the output.


#### Execute the churnrisk_flask_app.py application 

The `churnrisk_flask_app.py` starts a Flask application that provides REST methods for `authentication` and `predictions`.   This is an example of an application that takes requests and resturns a response.   The application could be enhanced to augment a request with additional data or save the input/output for future analysis and model improvements. 

Run:
'python churnrisk_flask_app.py'

This web application is started showing the URL, `http://0.0.0.0:8080/` or `http://<HOSTNAME>:8080/`

```
 * Serving Flask app "churnrisk_flask_app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
INFO:werkzeug: * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
INFO:werkzeug: * Restarting with stat
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: 709-910-698
``` 

The `authenticate` API requires a user, password, and url parameters.  The user and password are your CP4D user and password.    The url is the `<CP4D_URL>/v1/preauth/validateAuth` used to get the bearer token needed for the predictions API.  The application will cache the bearer token. 

`curl --location --request POST 'http://0.0.0.0:8080/authenticate?user=<USER_NAME>&password=<PASSWORD>&url=<CP4D_URL>/v1/preauth/validateAuth`

The predictions API requires a url and the prediction payload.  The url is the form `<CP4D_URL>/v4/deployments/<UID>/predictions` taken from from the churnrisk deployment in CP4D. 

```
curl --location --request POST 'http://0.0.0.0:8080/predict?url=https://dse-cp4d301-cluster1.datascienceelite.com/v4/deployments/f5c8d13b-d857-4f6d-9a7c-288f6dfe24fd/predictions' \
--header 'Content-Type: application/json' \
--data-raw '{"input_data":[{"fields":["AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[["Adult","F","M",2,25000,"N",5000,50,500,50,3.45,3,10,1500.0,0.0]]}]}'
```


#### Execute the churnrisk_localmodel.py application 

The `churnrisk_localmodel.py` loads the `churnrisk.pkl` file using pickle.load() method.  The `churnrisk.pkl` was created in the notebook using pickle.dump() method and saved in the project data a0ssets using the `project_lib` package.  A version of the `churnrisk.pkl` is included in the github project.  The file can also be downloaded from the project. 

Run: 
`python churnrisk_localmodel.py`

The application output:

```
load the churnrisk.pkl using pickle.load()
evaluate the loaded model using the model_eval.csv file.
predictions:  [1 0 0 0 0 2 2 1 1 1 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 1 2 0 1 2 2 0 1 0
 0 0 0 2 2 0 2 2 1 2 1 1 0 0 0 0 1 1 1 1 1 0 1 0 0 1 0 0 1 2 0 0 1 0 2 0 0
 0 0 1 1 2 0 0 0 0 2 0 0 1 1 0 0 1 0 1 1 1 1 1 0 0 0 1 2 2 0 0 1 0 0 2 0 1
 0 2 0 1 1 1 0 0 1 0 1 0 0 0 1 1 0 0 0 1 0 1 0 2 2 0 0 0 1 0 1 2 0 0 0 1 0
 0 0 1 0 0 0 1 0 0 1 1 0 0 1 0 0 0 0 2 0 0 2 0 2 1 0 1 0 1 1 2 0 0 0 0 0 2
 1 0 2 1 0 0 1 2 2 1 1 0 1 0 0 2 0 0 1 0 2 2 1 0 0 1 1 0 0 0 1 1 0 0 0 2 1
 1 0 1 0 1 2 1 0 0 0 0 1 0 0 2 0 1 1 1 0 0 0 1 1 0 1 0 0 0 0 2 2 1 0 0 0 1
 2 0 1 0 0 0 0 0 1 0 2 1 1 1 1 0 0 0 2 1 0 1 1 0 1 0 0 1 0 0 1 1 1 0 1 0 0
 0 1 0 1 1 1 2 1 0 0 1 1 0 1 0 0 0 0 1 1 0 1 0 2 0 0 0 1 1 0 0 0 1 1 0 2 1
 0 1 1 0 0 0 0 0 1 0 0 0 1 1 0 1 2 0 1 1 1 0 2 0 0 2 1 0 0 0 0 0 0 0 0 2 1
 1 0 2 2 2 0 2 1 1 0 0 0 0 1 0 0 0 1 0 1 2 1 0 2 0 0 1 2 0 0 1 1 1 0 1 0 0
 1 1 0 2 2 0 0 1 0 0 0 0 0 1 2 2 1 1 1 2 1 0 0 1 1 1 0 1 0 0 1 0 0 0 1 1 0
 2 0 1 0 0 0 0 2 0 1 1 1 0 2 1 2 2 0 1 2 0 2 0 1 2 0 2 0 0 0 0 1 0 0 1 0 0
 2 1 2 0 0 2 2 1 0 2 1 0 0 0 2 0 0 1 0 0 0 1 0 0 0 0 0 0 1 0 0 2 0 0 2 0 0
 1 2 1 2 0 0 1 1 0 0 1 1 0 2 1 2 1 1 0 2 0 0 0 0 1 0 0 0 0 0 2 0 0 0 0 0 1
 0 1 0 0 1 0 1 1 1 1 1 0 2 0 2 1 0 2 1 1 2 0 1 0 2 0 0 1 2 0 0 0 1 0 1 0 0
 0 0 0 0 1 0 1 1 0 1 0 0 0 1 0 0 0 0 0 0 1 0 1 0 0 0 1 1]
model accuracy:  0.9387096774193548
make a single prediction using a dataframe payload
prediction:  [2]
```



### Run an AutoAI experiment 

Start by pressing the `Add to `

![Add AutoAI experiment](images/add_autoai_experiment.png)

The AutoAI requires a name, churnrisk_autoai, in this case and it requires that a Machine Learning service be associated.   Follow the `Associate a Machine Learning service instance` link to select the ML service to associate.

![Associate ML service](images/associate_wml_service.png)

Press the `Reload` button after associating the ML service.

![Reload AutoAI](images/reload_autoai_experiment.png)

Create the AutoAI experiment.

![Create AutoAI experiment](images/create_autoai_experiment.png)

Select the data source from the Project.

![Add data source](images/autoai_add_data_source.png)

![Project data assets](images/project_data_assets.png)

Select churnrisk as the prediction field and press the `Run experiment` button.

![Run experiment](images/autoai_run_experiment.png)

The Experiment summary shows the progress.

![Experiment progress](images/autoai_experiment_progress.png)   

When the AutoAI experiment completes, select the top pipeline from the leader to add to the deployment space.

![AutoAI leaderboard](images/autoai_leaderboard.png)

The Pipeline4 provides information on the model evaluation, precision recall curve, threshold chart, model information, feature transformation and feature importance. 

![AutoAI model evaluation](images/autoai_model_evaluation.png)

Use the `Save as` button to as a `Model`.

![AutoAI save model](images/autoai_save_model.png)

In the `churnrisk` project there are two new assets.  The `churnrisk_autoai` experiment that was completed and the `churnrisk_autoai - P4 RandomForestClassifierEstimator` model that was saved.

![Model promotion](images/autoai_model_promote.png)

Promote the model to the `churnrisk_deployment_space`.


![Model promote to space](images/model_promote_to_space.png)

Go to the deployment space to deploy the model. 

![Model in space](images/autoai_model_in_deployment_space.png)

Use the rocket next to the model to deploy it. 

![Deploy model](images/deploy_rocket.png)

Create an online deployment for the model.

![Deploy model online](images/create_autoai_model_deployment.png)

You can see the AutoAI model in the list of deployments.

![Deployment list](images/churnrisk_deployment_list.png)

Test the deployed model using the form to input the data.

![Test AutoAI model](images/deployed_autoai_model_test.png)

You can also test the model using a json playload like this: 

```
{
	"input_data": [{
		"fields": ["ID", "AGE_GROUP", "GENDER", "STATUS", "CHILDREN", "ESTINCOME", "HOMEOWNER", "AGE", "TAXID", "CREDITCARD", "DOB", "ADDRESS_1", "ADDRESS_2", "CITY", "STATE", "ZIP", "ZIP4", "LONGITUDE", "LATITUDE", "TOTALDOLLARVALUETRADED", "TOTALUNITSTRADED", "LARGESTSINGLETRANSACTION", "SMALLESTSINGLETRANSACTION", "PERCENTCHANGECALCULATION", "DAYSSINCELASTLOGIN", "DAYSSINCELASTTRADE", "NETREALIZEDGAINS_YTD", "NETREALIZEDLOSSES_YTD"],
		"values": [
			[1, "Adult", "F", "M", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null]
		]
	}]
}
```
From your desktop, run the churnrisk_app.py application to call the AutoAI churnrisk model running in the cloud.

```
python churnrisk_autoai.py -a <YOUR APIKEY> -s <DEPLOYMENT SPACE NAME> -d "DEPLOYMENT NAME" -p <PAYLOAD>
```

```
python churnrisk_app.py -a _7cUoegW8Bt1ZLzgYbYms7o1uppelHJSCzwvnUegu0pB -s churnrisk_deployment_space -d churnrisk_autoai_model_deployment -p '{"input_data":[{"fields":["ID","AGE_GROUP","GENDER","STATUS","CHILDREN","ESTINCOME","HOMEOWNER","AGE","TAXID","CREDITCARD","DOB","ADDRESS_1","ADDRESS_2","CITY","STATE","ZIP","ZIP4","LONGITUDE","LATITUDE","TOTALDOLLARVALUETRADED","TOTALUNITSTRADED","LARGESTSINGLETRANSACTION","SMALLESTSINGLETRANSACTION","PERCENTCHANGECALCULATION","DAYSSINCELASTLOGIN","DAYSSINCELASTTRADE","NETREALIZEDGAINS_YTD","NETREALIZEDLOSSES_YTD"],"values":[[1,"Adult","F","M",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]]}]}'
```

Command output: 

```
deployment space:  churnrisk_deployment_space , id:  d39f197b-5193-40a5-aaec-c6cb34582740
deployment id:  988cfd06-975d-42ad-be76-f7772eca8b2f
deployment details:  {'entity': {'asset': {'id': '9684e5f7-2d75-4585-8d1d-bef2872b7b0b'}, 'custom': {}, 'deployed_asset_type': 'model', 'hybrid_pipeline_hardware_specs': [{'hardware_spec': {'name': 'S', 'num_nodes': 1}, 'node_runtime_id': 'auto_ai.kb'}], 'name': 'churnrisk_autoai_model_deployment', 'online': {}, 'space_id': 'd39f197b-5193-40a5-aaec-c6cb34582740', 'status': {'online_url': {'url': 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/988cfd06-975d-42ad-be76-f7772eca8b2f/predictions'}, 'state': 'ready'}}, 'metadata': {'created_at': '2020-10-12T16:06:09.757Z', 'id': '988cfd06-975d-42ad-be76-f7772eca8b2f', 'modified_at': '2020-10-12T16:06:09.757Z', 'name': 'churnrisk_autoai_model_deployment', 'owner': 'IBMid-550008YAWT', 'space_id': 'd39f197b-5193-40a5-aaec-c6cb34582740'}}
payload:  {'input_data': [{'fields': ['ID', 'AGE_GROUP', 'GENDER', 'STATUS', 'CHILDREN', 'ESTINCOME', 'HOMEOWNER', 'AGE', 'TAXID', 'CREDITCARD', 'DOB', 'ADDRESS_1', 'ADDRESS_2', 'CITY', 'STATE', 'ZIP', 'ZIP4', 'LONGITUDE', 'LATITUDE', 'TOTALDOLLARVALUETRADED', 'TOTALUNITSTRADED', 'LARGESTSINGLETRANSACTION', 'SMALLESTSINGLETRANSACTION', 'PERCENTCHANGECALCULATION', 'DAYSSINCELASTLOGIN', 'DAYSSINCELASTTRADE', 'NETREALIZEDGAINS_YTD', 'NETREALIZEDLOSSES_YTD'], 'values': [[1, 'Adult', 'F', 'M', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]}]}
{'predictions': [{'fields': ['prediction', 'probability'],
                  'values': [['High',
                              [0.6926862955911713, 0.0, 0.3073137044088286]]]}]}
```
