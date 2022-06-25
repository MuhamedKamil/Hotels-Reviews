import pandas as pd
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


class Classifier:
    def __init__(self, data_path):
        self.data_path = data_path
        self.dataset = pd.read_csv(self.data_path)
        self.vectorizer = TfidfVectorizer()
        self.clf = LogisticRegression(solver="liblinear")
        self.model = Pipeline([('vectorizer', self.vectorizer), ('classifier', self.clf)])

    def clean_text(self, text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text

    def get_training_testing_data(self):
        self.dataset.drop(columns=['User_ID', 'Browser_Used', 'Device_Used'], inplace=True)
        self.dataset['cleaned_description'] = pd.DataFrame(self.dataset.Description.apply(lambda x: self.clean_text(x)))
        X = self.dataset.cleaned_description
        Y = self.dataset.Is_Response
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=225)

        return X_train, X_test, y_train, y_test

    def train(self, X_train, Y_train):
        self.model.fit(X_train, Y_train)

    def evaluate(self, X_test, Y_test):
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(predictions, Y_test)
        precision = precision_score(predictions, Y_test, average='weighted')
        recall = recall_score(predictions, Y_test, average='weighted')
        return accuracy, precision, recall

    def predict(self, text):
        result = self.model.predict(text)
        return result
