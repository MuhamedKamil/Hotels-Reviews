from flask import Flask, render_template, request
from data import Data
from analyzer import Analyzer
import json
from classifier import Classifier

app = Flask(__name__)
"Required Part"
path = "./dataset/7282_1.csv"
pathForTrainingData = "./dataset/train.csv"
dataset = Data(path)
dataset.preprocessData()
hotel_names = dataset.getUniqueHotelNames()
analyzer = Analyzer()
dataset.indexDataToElastic()
# --------------------------------------------------------------------------
"Bonus Part"
"""
logisticRegressionCLS = Classifier(pathForTrainingData)
X_train, X_test, Y_train, Y_test = logisticRegressionCLS.get_training_testing_data()
logisticRegressionCLS.train(X_train, Y_train)
"""


@app.route('/')
def home():
    return render_template('index.html', hotel_names=hotel_names)


@app.route('/Score', methods=['POST', 'GET'])
def calculate_score():
    if request.method == 'POST':
        selected_hotel = request.form.get('comp_select')
        hotel_reviews = dataset.getSpecificHotelReviews(hotel_name=selected_hotel)
        pos, neg = analyzer.getNormalizedScores(hotel_reviews)
        hotel_doc = dataset.getHotelByName(selected_hotel)
        response = json.dumps(hotel_doc, sort_keys=True, indent=4, separators=(',', ': '))

        return render_template('index.html', hotel_names=hotel_names, selected_hotel=selected_hotel, pos=pos, neg=neg,
                               response=response)
    else:
        return render_template('index.html', hotel_names=hotel_names)


if __name__ == '__main__':
    app.run()
