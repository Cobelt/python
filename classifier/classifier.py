from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

from features_extraction import load_tweets

import pandas as pd
import numpy as np

import pickle as pkl

np.random.seed(0)

file_name = 'clf_params.txt'
nb_features = 0

# regex = '(?P<key>[a-z_]+)=((?P<int>\d+)|(?P<bool>True|False)|(?P<none>None)|(?P<string>[a-zA-Z]+))'


def get_clf():
    clf = pkl.load(open("trained_clf.pkl", "rb"))
    print(clf)
    return clf


# def create_clf():
#     with open(file_name) as file:
#         params = {}
#         for line in file:
#             match = re.search(regex, line)
#
#             if match.group('int'):
#                 params[match.group('key')] = int(match.group('int'))
#             elif match.group('bool'):
#                 params[match.group('key')] = bool(match.group('bool'))
#             elif match.group('none'):
#                 params[match.group('key')] = None
#             elif match.group('string'):
#                 params[match.group('key')] = match.group('string')
#
#     global nb_features
#     nb_features = params
#     del params["nb_features"]
#
#     print('Classifier parameters:', params)
#
#     clf = RandomForestClassifier(**params)
#     return clf


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
    train_tab, test_tab = [], []
    is_train_array = np.random.randint(2, size=data.shape[0])
    print(is_train_array)
    for i in len(data):
        if is_train_array[i] == 0:
            np.append(test_tab, data[i], axis=0)
        else:
            np.append(train_tab, data[i], axis=0)

    return train_tab, test_tab


def static_train_attribution(data):
    third_quartile = int(data.shape[0] * 3/4)

    train_tab = data[:third_quartile]
    test_tab = data[third_quartile:]

    return train_tab, test_tab, third_quartile


def train_and_test(_data, _target, _target_names):

    # Train Part ->
    # train_tab, test_tab = rand_train_attribution(_data)
    train_tab, test_tab, third_quartile = static_train_attribution(_data)
    train_tab_target = _target[:third_quartile]

    print('Quantity of data from train:', len(train_tab))
    print('Quantity of data for test:', len(test_tab))

    print(train_tab_target)
    clf.fit(train_tab, train_tab_target)

    pkl.dump(clf, open("trained_clf.pkl", "wb"), protocol=pkl.HIGHEST_PROTOCOL)
    # <-

    test(test_tab)

    features_importance(train_tab)


def test(test_tab):

    # predicts = _target_names[clf.predict(test_tab)]
    predicts = clf.predict(test_tab)

    # tableau a deux entrées pour afficher les erreurs
    # print(pd.crosstab(test_tab['species'], predicts, rownames=['Actual Species'], colnames=['Predicted Species']).head())

    calculate_accuracy(predicts, test_tab)


def predict(data):
    features = data.columns[:4]
    # predicts = iris.target_names[clf.predict(data[features])]
    # print(predicts)


# Partie test

clf = get_clf()

# iris = load_iris()
# data = pd.DataFrame(iris.data, columns=iris.feature_names)
#
# # iris.target = 0, 1 ou 2 / iris.target_names contient les correspondances
# # Nous ce serait des 0 ou 1 et ["positif", "negatif"]
# data['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
#
# train_and_test(data)


tweets = load_tweets()
data = tweets['data']
target = np.array(tweets['target'])
# target = np.vstack(tweets['target'])

len_array = data.shape[1]
# np.append(data, target, axis=1)

train_and_test(data, target, ["negative", "neutral", "positive"])
