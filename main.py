# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



import utils
import SQLPipeline
import DataProcessing
import Models




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
CREATE_CLICKS_SCHEMA = f"CREATE SCHEMA IF NOT EXISTS clicks_schema;"
CREATE_LEADS_SCHEMA =  f"CREATE SCHEMA IF NOT EXISTS leads_schema;"
CREATE_OFFERS_SCHEMA =  f"CREATE SCHEMA IF NOT EXISTS offers_schema;"
schemaQueries = [CREATE_CLICKS_SCHEMA, CREATE_LEADS_SCHEMA, CREATE_OFFERS_SCHEMA]
tables = ["clicks", "leads", "offers"]
schema = ["clicks_schema", "leads_schema", "offers_schema"]
data_list = [clicks, leads, offers]
target_variable = "clicked_at"


select_query = "SELECT leads.index, leads.lead_uuid, leads.requested, leads.loan_purpose, leads.annual_income,\
offers.offer_id, offers.apr, offers.lender_id, clicks.clicked_at \
FROM leads_schema.LEADS \
LEFT JOIN offers_schema.OFFERS \
ON (leads_schema.LEADS.lead_uuid = offers_schema.OFFERS.lead_uuid) \
LEFT JOIN clicks_schema.CLICKS \
ON (offers_schema.OFFERS.offer_id = clicks_schema.CLICKS.offer_id) \
ORDER BY lead_uuid"


cat_vars = ['loan_purpose', 'lender_id']

filename = 'trained_model.pkl'
column_name_file = "columns.txt"

test_size = 0.3




#data['requested'] = MinMaxScaler().fit_transform(data[['requested']])
#data['annual_income'] = MinMaxScaler().fit_transform(data[['annual_income']])



datapipeline = SQLPipeline.Pipeline(param_dic)
datapipeline.createSchemas(schemaQueries)
datapipeline.createTables(tables, schema, data_list)


data = datapipeline.selectData(select_query)

data = DataProcessing.dropColumns(data)
data = DataProcessing.updateTargetValues(data)
data = DataProcessing.dropRows(data)

data_final = DataProcessing.createDummyColumns(data, cat_vars)



data_final[target_variable]=data_final[target_variable].astype('int')

X_train, X_test, y_train, y_test = DataProcessing.splitTrainTest(data_final, test_size)


"""SMOTE"""
os_data_X, os_data_y = DataProcessing.getSMOTE(X_train, y_train)

selected_columns = DataProcessing.selectFeatures(os_data_X, os_data_y)

print("selected columns:" + selected_columns)

os_data_X= os_data_X[selected_columns]
os_data_y= os_data_y[target_variable]
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

logreg.save_columns(column_name_file, selected_columns)



"""Baseline model"""


datapoint = {'requested': 100000, 'annual_income': 0, 'loan_purpose': 'business', 'apr': 199.000, 'lender_id': '417'}








