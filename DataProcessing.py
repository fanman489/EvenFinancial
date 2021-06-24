from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


def updateTargetValues(data):

    data.loc[data['clicked_at'].notnull(), 'clicked_at'] = 1
    data.loc[data['clicked_at'].isnull(), 'clicked_at'] = 0

    return data

def dropColumns(data):

    return data.drop(columns=['index', 'offer_id', 'lead_uuid'])


def dropRows(data):

    return data.dropna()



def createDummyColumns(data, cat_vars):


    for var in cat_vars:
        #cat_list = 'var' + '_' + var
        cat_list = pd.get_dummies(data[var], prefix=var)
        data1 = data.join(cat_list)
        data = data1

    data_vars = data.columns.tolist()
    to_keep = [i for i in data_vars if i not in cat_vars]

    data_final = data[to_keep]
    return data_final



def splitTrainTest(data, test_size):
    X = data.loc[:, data.columns != 'clicked_at']
    y = data.loc[:, data.columns == 'clicked_at']
    return train_test_split(X, y, test_size=test_size, random_state=0)


def getSMOTE(X_train, y_train):
    os = SMOTE(random_state=0)


    columns = X_train.columns
    os_data_X, os_data_y = os.fit_resample(X_train, y_train)

    os_data_X = pd.DataFrame(data=os_data_X, columns=columns)
    os_data_y = pd.DataFrame(data=os_data_y, columns=['clicked_at'])
    # we can Check the numbers of our data
    print("length of oversampled data is ", len(os_data_X))
    print("Number of no subscription in oversampled data", len(os_data_y[os_data_y['clicked_at'] == 0]))
    print("Number of subscription", len(os_data_y[os_data_y['clicked_at'] == 1]))
    print("Proportion of no subscription data in oversampled data is ",
          len(os_data_y[os_data_y['clicked_at'] == 0]) / len(os_data_X))
    print("Proportion of subscription data in oversampled data is ",
          len(os_data_y[os_data_y['clicked_at'] == 1]) / len(os_data_X))

    return os_data_X, os_data_y


"""Perform RFE to select features"""
def selectFeatures(os_data_X, os_data_y):
    data_final_vars = os_data_X.columns.values.tolist()
    y_columns = ['clicked_at']
    X_columns = [i for i in data_final_vars if i not in os_data_y.columns]


    logreg = LogisticRegression()
    rfe = RFE(logreg, n_features_to_select=30)
    rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
    print(X_columns)
    print(rfe.support_)
    print(rfe.ranking_)

    selected_columns = [y for x, y in zip(rfe.ranking_, X_columns) if x <= 7]

    return selected_columns