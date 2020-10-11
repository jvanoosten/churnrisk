# Save the pipeline with pickle
import pandas as pd
import numpy as np
import pickle
import sklearn.pipeline

filename = 'churnrisk.pkl'
print('load the ' + filename + ' using pickle.load()')
loaded_model = pickle.load(open(filename, 'rb'))

eval = 'model_eval.csv'
X_test = pd.read_csv(eval)
loaded_model = pickle.load(open(filename, 'rb'))
print('evaluate the loaded model using the ' + eval + ' file.')
predictions = loaded_model.predict(X_test)
print('predictions: ', predictions)

y_test = [1, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 2, 0, 1, 2, 2, 0, 1, 0, 0, 0, 0, 2, 2, 0, 2, 0, 1, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 2, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 2, 2, 0, 0, 1, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 1, 0, 1, 2, 1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 0, 2, 1, 0, 0, 1, 2, 2, 1, 1, 0, 1, 0, 0, 2, 0, 0, 1, 0, 2, 2, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 2, 0, 2, 2, 1, 1, 0, 1, 0, 1, 2, 2, 0, 0, 0, 0, 1, 2, 0, 2, 0, 1, 1, 1, 0, 2, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 2, 0, 2, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 2, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 2, 1, 2, 0, 1, 1, 1, 0, 2, 0, 0, 2, 1, 0, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 2, 0, 2, 0, 2, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 0, 2, 0, 0, 1, 2, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 2, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 2, 1, 1, 0, 2, 0, 1, 0, 0, 0, 0, 2, 0, 1, 1, 1, 0, 2, 1, 2, 2, 0, 1, 2, 0, 2, 2, 1, 2, 0, 0, 0, 0, 2, 0, 1, 2, 0, 1, 0, 0, 2, 1, 2, 0, 0, 0, 2, 1, 0, 2, 1, 0, 0, 0, 2, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 2, 0, 0, 2, 0, 0, 1, 2, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 2, 1, 2, 1, 1, 0, 2, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 2, 2, 0, 2, 1, 0, 0, 1, 1, 2, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 2, 1, 2, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1]

# Find the accuracy 
accuracy = loaded_model.score(X_test,y_test)
print('model accuracy: ', accuracy)

# Make a single prediction
titles = ['id', 'AGE_GROUP', 'GENDER', 'STATUS', 'CHILDREN', 'ESTINCOME', 'HOMEOWNER', 'TOTALDOLLARVALUETRADED', 'TOTALUNITSTRADED', 'LARGESTSINGLETRANSACTION', 'SMALLESTSINGLETRANSACTION', 'PERCENTCHANGECALCULATION', 'DAYSSINCELASTLOGIN', 'DAYSSINCELASTTRADE', 'NETREALIZEDGAINS_YTD', 'NETREALIZEDLOSSES_YTD']
payload = [[1, "Adult","F","M",2,25000,"N",5000,50,500,50,3.45,3,10,1500.0,0.0]]
df = pd.DataFrame(payload, columns=titles).set_index('id')
df.append(payload)
# print(df)
print('make a single prediction using a dataframe payload')
single = loaded_model.predict(df)
print('prediction: ', single)
