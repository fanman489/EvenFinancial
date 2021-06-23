

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
        self.selected_columns = None


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


    def load_model(self, location):
        self.filename = location

    """Predict a single lead"""
    def predict_JSON_single(self, data):

        model = pickle.load(open(self.filename, 'rb'))

        with open("file.txt", 'r') as f:
            self.selected_columns = [line.rstrip('\n') for line in f]
        input = self.process_datapoint(data)

        """
        for (columnName, columnData) in output.iteritems():
            print('Colunm Name : ', columnName)
            print('Column Contents : ', columnData.values)
        """
        y_pred = model.predict_proba(input)

        return str(y_pred[0][0])


    """Predict from a list of leads"""
    def predict_JSON_multiple(self, data):

        model = pickle.load(open(self.filename, 'rb'))
        output = []

        with open("file.txt", 'r') as f:
            self.selected_columns = [line.rstrip('\n') for line in f]


        for data_point in data:

            input = self.process_datapoint(data_point)

            """
            for (columnName, columnData) in output.iteritems():
                print('Colunm Name : ', columnName)
                print('Column Contents : ', columnData.values)
            """
            y_pred = model.predict_proba(input)
            output.append(str(y_pred[0][0]))

        return ' '.join(output)

    #print("predictions", predict(datapoint))



    def process_datapoint(self, data_point):
        input = pd.DataFrame(columns=self.selected_columns)
        input.loc[0] = 0

        if 'requested' in self.selected_columns:
            input['requested'] = data_point['requested']
        if 'requested' in self.selected_columns:
            input['annual_income'] = data_point['annual_income']
        if 'requested' in self.selected_columns:
            input['apr'] = data_point['apr']

        purpose = 'loan_purpose' + '_' + data_point['loan_purpose']

        if purpose in self.selected_columns:
            input[purpose] = 1
        lender = 'lender_id' + '_' + data_point['lender_id']
        if lender in self.selected_columns:
            input[lender] = 1

        return input

