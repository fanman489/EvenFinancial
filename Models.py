

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle
import pandas as pd

from sklearn.metrics import classification_report


class prediction_model():
    def __init__(self):
        self.logreg = LogisticRegression()
        self.columns = []
        self.filename = None


    def fit(self, X, y):
        return self.logreg.fit(X, y.ravel())



    def predict(self, X):
        return self.logreg.predict(X)

    def predict_proba(self, X):
        return self.logreg.predict_proba(X)


    def evaluate_accuracy(self, labels, predictions):
        accuracy = metrics.accuracy_score(labels, predictions)

        return accuracy

    def getparameters(self):
        return self.logreg.coef_

    def saveModel(self, filename):
        self.filename = 'trained_model.pkl'
        pickle.dump(self.logreg, open(self.filename, 'wb'))

    def evaluate_confusion_matrix(self, labels, predictions):

        confusion_matrix = metrics.confusion_matrix(labels, predictions)
        return confusion_matrix

    def evaluate_classification_report(self, labels, predictions):
        return classification_report(labels, predictions)


    def save_columns(self, file_name, selected_columns):


        with open(file_name, 'w') as f:
            for s in selected_columns:
                f.write(str(s) + '\n')

    def predict_from_JSON(data):

        model = pickle.load(open(self.filename, 'rb'))

        length_lender = len(data['lender_id'])

        with open("file.txt", 'r') as f:
            selected_columns = [line.rstrip('\n') for line in f]

        output = pd.DataFrame(columns=selected_columns)

        print(length_lender, data['lender_id'])

        output.loc[0] = 0

        if 'requested' in selected_columns:
            output['requested'] = data['requested']
        if 'requested' in selected_columns:
            output['annual_income'] = data['annual_income']
        if 'requested' in selected_columns:
            output['apr'] = data['apr']

        purpose = 'loan_purpose' + '_' + data['loan_purpose']

        print(data['loan_purpose'])
        if purpose in selected_columns:
            output[purpose] = 1
        lender = 'lender_id' + '_' + data['lender_id']
        if lender in selected_columns:
            output[lender] = 1

        for (columnName, columnData) in output.iteritems():
            print('Colunm Name : ', columnName)
            print('Column Contents : ', columnData.values)
        y_pred = model.predict_proba(output)

        return str(y_pred[0][0])

    #print("predictions", predict(datapoint))

