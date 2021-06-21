# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





from sqlalchemy import create_engine
import pandas as pd
import utils

from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
import SQLPipeline
import DataProcessing
import Models



'non esential'
import seaborn as sns
import matplotlib.pyplot as plt

param_dic = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "fantheman48"
}


clicks = utils.readParquet('..\Data\ds_clicks.parquet.gzip')
leads = utils.readParquet('..\Data\ds_leads.parquet.gzip')
offers = utils.readParquet('..\Data\ds_offers.parquet.gzip')



# Build Query Strings:
CREATE_CLICKS_SCHEMA = f"CREATE SCHEMA IF NOT EXISTS clicks;"
CREATE_LEADS_SCHEMA =  f"CREATE SCHEMA IF NOT EXISTS leads;"
CREATE_OFFERS_SCHEMA =  f"CREATE SCHEMA IF NOT EXISTS offers;"
schemaQueries = [CREATE_CLICKS_SCHEMA, CREATE_LEADS_SCHEMA, CREATE_OFFERS_SCHEMA]



select_query = "SELECT leads.index, leads.lead_uuid, leads.requested, leads.loan_purpose, leads.annual_income,\
offers.offer_id, offers.apr, offers.lender_id, clicks.clicked_at \
FROM leads.LEADS \
LEFT JOIN offers.OFFERS \
ON leads.LEADS.lead_uuid = offers.OFFERS.lead_uuid \
LEFT JOIN clicks.CLICKS \
ON offers.OFFERS.offer_id = clicks.CLICKS.offer_id \
ORDER BY leads.lead_uuid"

cat_vars = ['loan_purpose', 'lender_id']

filename = 'trained_model.pkl'
column_name = "columns.txt"

test_size = 0.3




#data['requested'] = MinMaxScaler().fit_transform(data[['requested']])
#data['annual_income'] = MinMaxScaler().fit_transform(data[['annual_income']])



datapipeline = SQLPipeline.Pipeline(param_dic)
datapipeline.createSchemas(schemaQueries)


data = datapipeline.selectData(select_query)

data = DataProcessing.dropColumns(data)
data = DataProcessing.updateTargetValues(data)
data = DataProcessing.dropRows(data)

print(data)
data_final = DataProcessing.createDummyColumns(data, cat_vars)



data_final['clicked_at']=data_final['clicked_at'].astype('int')

X_train, X_test, y_train, y_test = DataProcessing.splitTrainTest(data_final, test_size)


"""SMOTE"""
os_data_X, os_data_y = DataProcessing.getSMOTE(X_train, y_train)

selected_columns = DataProcessing.selectFeatures(os_data_X, os_data_y)

print(selected_columns)

os_data_X= os_data_X[selected_columns]
os_data_y= os_data_y['clicked_at']
X_train= X_train[selected_columns]
X_test= X_test[selected_columns]


print(os_data_X, os_data_y)

import statsmodels.api as sm
logit_model=sm.Logit(os_data_y,os_data_X)
result=logit_model.fit()






logreg = Models.prediction_model()


logreg.fit(os_data_X, os_data_y.ravel())
predicted_classes = logreg.predict(X_test)


print(logreg.evaluate_accuracy(y_test, predicted_classes))

parameters = logreg.getparameters()
print(parameters)

logreg.saveModel(filename)

y_pred = logreg.predict_proba(X_test)
print(y_pred)


confusion_matrix = logreg.evaluate_confusion_matrix(y_test, predicted_classes)
print(confusion_matrix)

classification = logreg.evaluate_classification_report(y_test, predicted_classes)
print(classification)

logreg.save_columns(column_name, selected_columns)



"""Baseline model"""


datapoint = {'requested': 100000, 'annual_income': 0, 'loan_purpose': 'business', 'apr': 199.000, 'lender_id': '417'}








