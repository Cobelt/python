from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# import ./dataset

import pandas as pd
import numpy as np

import re

np.random.seed(0)

file_name = 'clf_params.txt'
nb_features = 0

regex = '(?P<key>[a-z_]+)=((?P<int>\d+)|(?P<bool>True|False)|(?P<none>None)|(?P<string>[a-zA-Z]+))'


def create_clf():
    with open(file_name) as file:
        params = {}
        for line in file:
            match = re.search(regex, line)

            if match.group('int'):
                params[match.group('key')] = int(match.group('int'))
            elif match.group('bool'):
                params[match.group('key')] = bool(match.group('bool'))
            elif match.group('none'):
                params[match.group('key')] = None
            elif match.group('string'):
                params[match.group('key')] = match.group('string')

    global nb_features
    nb_features = params
    del params["nb_features"]

    print('clf_params =', params)

    clf = RandomForestClassifier(**params)
    return clf


def calculate_accuracy(predicts, test_tab):
    errors = [pred for pred, test in zip(predicts, test_tab) if pred != test]
    print('\nErrors quantity :', len(errors), '\n')

    percentError = 100 * (len(errors) / len(test_tab))
    accuracy = 100 - percentError

    print('Accuracy:', round(accuracy, 2), '%.\n')


def features_importance(features):
    sortedFeat = list(zip(clf.feature_importances_, features))
    sortedFeat.sort(reverse=True)

    print('Sorted features by importance :')
    for item in sortedFeat:
        print(item[1], '=>', round(item[0]*100, 2), '%')


def rand_train_attribution(data):
    # 0 or 1 at each row with 75% maximum of "1"
    data['is_train'] = np.random.uniform(0, 1, len(data)) <= .75


def train_and_test(data):

    # Train Part ->
    rand_train_attribution(data)

    train_tab = data[data['is_train']==True]
    test_tab = data[data['is_train']==False]

    print('Quantity of data from train:', len(train_tab))
    print('Quantity of data for test:', len(test_tab))

    features = data.columns[:4]
    known = pd.factorize(train_tab['species'])[0]

    clf.fit(train_tab[features], known)
    # <-


    # Test Part ->
    predicts = iris.target_names[clf.predict(test_tab[features])]

    # tableau a deux entrées pour afficher les erreurs
    # print(pd.crosstab(test_tab['species'], predicts, rownames=['Actual Species'], colnames=['Predicted Species']).head())

    calculate_accuracy(predicts, test_tab['species'])
    # <-

    features_importance(train_tab[features])


def predict(data):
    features = data.columns[:4]
    predicts = iris.target_names[clf.predict(data[features])]
    print (predicts)


# Partie test

clf = create_clf()

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)

# iris.target = 0, 1 ou 2 / iris.target_names contient les correspondances
# Nous ce serait des 0 ou 1 et ["positif", "negatif"]
data['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

train_and_test(data)


# tweets = load_tweets()
# data = np.DataFrame(tweets.data, columns=tweets.feature_names)
# data['temper'] = tweets.target

# train_and_test(data)
