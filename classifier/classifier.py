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
    # print(clf)
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


def calculate_accuracy(_predicts, _targets):
    cpt_pos_pred, cpt_neg_pred, cpt_pos_targ, cpt_neg_targ = 0, 0, 0, 0
    for pred in _predicts:
        if pred == 1:
            cpt_pos_pred += 1
        else:
            cpt_neg_pred += 1

    for targ in _targets:
        if targ == 1:
            cpt_pos_targ += 1
        else:
            cpt_neg_targ += 1

    print('Positive : Target =', cpt_pos_targ,
          '; Predicted =', cpt_pos_pred)

    print('Negative : Target =', cpt_neg_targ,
          '; Predicted =', cpt_neg_pred)

    errors = [pred for pred, test in zip(_predicts, _targets) if pred != test]
    print('\nErrors quantity :', len(errors), '\n')

    percent_error = 100 * (len(errors) / len(_targets))
    accuracy = 100 - percent_error

    print('Accuracy:', round(accuracy, 2), '%.\n')


def features_importance(_features):
    sorted_feat = list(zip(clf.feature_importances_, _features))
    sorted_feat.sort(reverse=True)

    print('Sorted features by importance :')
    for item in sorted_feat:
        print(item[1], '=>', round(item[0]*100, 2), '%')


def rand_train_attribution(_data):
    # 0 or 1 at each row with 75% maximum of "1"
    train_tab, test_tab = [], []
    is_train_array = np.random.randint(2, size=_data.shape[0])
    print(is_train_array)
    for i in len(_data):
        if is_train_array[i] == 0:
            np.append(test_tab, _data[i], axis=0)
        else:
            np.append(train_tab, _data[i], axis=0)

    return train_tab, test_tab


def static_train_attribution(_data):
    third_quartile = int(_data.shape[0] * 3/4)

    train_tab = _data[:third_quartile]
    test_tab = _data[third_quartile:]

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

    test(test_tab, target[third_quartile:])

    features_importance(train_tab)


def test(_test_tab, _targets):

    # predicts = _target_names[clf.predict(test_tab)]
    predicts = clf.predict(_test_tab)

    calculate_accuracy(predicts, _targets)
    validate_test(_test_tab, _targets, predicts)


def validate_test(_test_tab, _targets, predicts):

    test_targets = _targets[:]
    to_fit_test_tab = _test_tab
    to_fit_targets = _targets
    for i in range(len(predicts)):
        if predicts[i] != _targets[i]:
            np.delete(to_fit_test_tab, i, 0)
            np.delete(to_fit_targets, i, 0)

    clf.fit(to_fit_test_tab, to_fit_targets)

    pkl.dump(clf, open("trained_clf.pkl", "wb"), protocol=pkl.HIGHEST_PROTOCOL)


def predict(data):

    predicts = clf.predict(data)
    return predicts




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

# np.append(data, target, axis=1)

# train_and_test(data, target, ["negative", "neutral", "positive"])

test(data, target)