# coding=utf-8

from sklearn.feature_extraction.text import TfidfVectorizer

from polyglot.text import Text
from polyglot.detect import Detector

import pandas
import numpy

from scipy.sparse import hstack


dataset = pandas.read_csv("../preprocessing/preprocess_tweet_file.csv")


def polarity_average_vectorizer(dataset):
    vector = numpy.zeros([len(dataset), 1])
    index = 0
    for sentence in dataset:
        text = Text(sentence.encode('utf-8'))
        sum = 0
        words_count = len(text.words)
        for word in text.words:
            try:
                sum += word.polarity
            except(ValueError, UnicodeDecodeError) as e:
                sum += 0
                print(e)
        vector[index][0] = sum / words_count
        print(vector[index][0])
        index +=1
    return vector


def polarity_sum_vectorizer(dataset):
    vector = numpy.zeros([len(dataset), 1])
    index = 0
    for sentence in dataset:
        text = Text(sentence.encode('utf-8'))
        sum = 0
        for word in text.words:
            try:
                sum += word.polarity
            except(ValueError, UnicodeDecodeError) as e:
                sum += 0
                print(e)
        vector[index][0] = sum
        print(vector[index][0])
        index +=1
    return vector


def get_data():
    return dataset.loc[0:,"clean_text"]


def get_target():
    # return nothing if not known ?
    return dataset['polarity']


def load_tweets():

    tweets_obj = {}

    X = get_data()
    tweets_obj['target'] = get_target()

    tfidfvectorizer = TfidfVectorizer(encoding='utf-8',
                                 decode_error='strict',
                                 strip_accents=None,
                                 analyzer='char',
                                 stop_words='english',
                                 ngram_range=(2,4),
                                 lowercase=True,
                                 max_features=None,
                                 binary=False,
                                 norm=None,
                                 use_idf=True,
                                 smooth_idf=False,
                                 min_df=0.1,
                                 max_df=0.8,
                                 sublinear_tf=True)

    tfidf = tfidfvectorizer.fit_transform(X.values.astype(str))
    polarity_sum = polarity_sum_vectorizer(X)
    polarity_average = polarity_average_vectorizer(X)

    features = hstack(tfidf, polarity_sum)
    features = hstack(features, polarity_average)

    tweets_obj['data'] = features.toarray()
    return tweets_obj



#X_transform_test = numpy.empty(shape=[len(X), 1])

# print(X_transform)
# print(X_transform_test)
# print(type(X_transform))
# print(type(X_transform_test))

# X_concat = hstack((X_transform, X_transform_test))
# print(X_transform)
# print(X_transform_test)
# print(X_concat)

# import sent2vec
#
# model = sent2vec.sent2vecModel()
# model.load_model('twitter_bigrams.bin')
# emb = model.embed_sentence("once upon a time .")








