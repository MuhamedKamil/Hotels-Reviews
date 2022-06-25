from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


class Analyzer:
    def __init__(self):
        self.analyzer = NaiveBayesAnalyzer()

    def getSentiment(self, text):
        blob = TextBlob(text, analyzer=self.analyzer)
        return blob.sentiment

    def getPosScore(self, sentiment):
        return sentiment.p_pos

    def getNegScore(self, sentiment):
        return sentiment.p_neg

    def getNormalizedScores(self, reviewsForHotel):
        length = len(reviewsForHotel)
        SentimentForReviews = reviewsForHotel.apply(self.getSentiment)
        total_pos = 0.0
        total_neg = 0.0
        pos_score = 0.0
        neg_score = 0.0
        for sent in SentimentForReviews:
            total_pos += self.getPosScore(sent)
            total_neg += self.getNegScore(sent)
        if length != 0:
            pos_score = total_pos / length
            neg_score = total_neg / length

        return pos_score, neg_score
