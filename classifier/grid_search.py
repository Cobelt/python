import numpy as np

from time import time
import io
import json
import pandas as pd

import pickle as pkl

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


# Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters:", results['params'][candidate])


def find_best_classifier_and_train(X, y):

    nb_features = len(pd.DataFrame(X).columns)

    clf = RandomForestClassifier()

    param_grid = {"n_estimators": [200, 300],
                  "max_depth": [9],
                  "min_samples_split": [2, 3, 4],
                  "min_samples_leaf": [1, 4],
                  "bootstrap": [True, False]}

    grid_search = GridSearchCV(clf, cv = 5, param_grid=param_grid)
    start = time()
    grid_search.fit(X, y)

    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)

    # wb write binary
    pkl.dump(grid_search, open("trained_clf.py", "wb"))

    return grid_search


# Partie test

iris = load_iris()
X, y = iris.data, iris.target
find_best_classifier_and_train(X, y)
