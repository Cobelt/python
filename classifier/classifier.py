from features_extraction import load_tweets
from grid_search import find_best_classifier_and_train

import numpy as np

import pickle as pkl

from time import time

np.random.seed(0)

nb_features = 0


def get_clf():
    clf = pkl.load(open("trained_clf.pkl", "rb"))
    # print(clf)
    return clf


def calculate_accuracy(_predicts, _targets):
    cpt_pos_pred, cpt_neg_pred, cpt_pos_targ, cpt_neg_targ = 0, 0, 0, 0
    for pred, targ in zip(_predicts, _targets):
        if pred == 1 or pred == "1":
            cpt_pos_pred += 1
        elif pred == -1 or pred == "-1":
            cpt_neg_pred += 1

        if targ == 1 or targ == "1":
            cpt_pos_targ += 1
        elif pred == -1 or targ == "-1":
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

    sorted_feat = list(zip(clf.best_estimator_.feature_importances_, _features))
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


def train_and_test(_data, _target):

    # Train Part ->
    train_tab, test_tab, third_quartile = static_train_attribution(_data)
    train_tab_target = _target[:third_quartile]

    train(train_tab, train_tab_target)
    test(test_tab, target[third_quartile:], True)


def train(_data, _target):
    print('Quantity of data from train:', len(_data))

    start = time()
    clf.fit(_data, _target)
    print("Took %.2f seconds to train on %d tweets" % (time() - start, len(_data)))

    pkl.dump(clf, open("trained_clf.pkl", "wb"), protocol=pkl.HIGHEST_PROTOCOL)

    # features_importance(_data)


def test(_data, _target, train_corrects):
    print('Quantity of data for test:', len(_data))

    start = time()
    predicts = clf.predict(_data)
    print("Took %.2f seconds to predict %d tweets" % (time() - start, len(_data)))

    calculate_accuracy(predicts, _target)

    if train_corrects:
        validate_test(_data, _target, predicts)


def validate_test(_test_tab, _targets, predicts):

    to_fit_test_tab = _test_tab
    to_fit_targets = _targets
    for i in range(len(predicts)):
        if predicts[i] != _targets[i]:
            np.delete(to_fit_test_tab, i, 0)
            np.delete(to_fit_targets, i, 0)

    train(to_fit_test_tab, to_fit_targets)


def predict(_data):

    predicts = clf.predict(_data)

    return predicts



tweets = load_tweets()
data = tweets['data']
data = data[:,:195]
target = np.array(tweets['target'])


# find_best_classifier_and_train(data, target)

clf = get_clf()
# train(data, target)
test(data, target, False)