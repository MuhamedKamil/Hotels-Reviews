# Hotels-Reviews
Dataset Link https://www.kaggle.com/datasets/datafiniti/hotel-reviews

------------
The project consists of three parts:
------------
1- Hotel Sentiment Analyzer

A service with one endpoint to get the total sentiment for a specific hotel by Calculating the normalized total score for the hotel
reviews which can be positive or negative.

2- Hotel indexer

Using elasticsearch to index all data founded in the dataset for hotel. each hotel have only one document with all its data.

3- simple classifier
I built a simple logistic regression classifier for sentiment analysis to classify hotel guest reviews using data included in the dataset folder

Dataset Link https://www.kaggle.com/anu0012/hotel-review/data

------------
Installation
------------
1- pip install -r requirements.txt

2- python server.py


