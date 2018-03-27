import numpy as np

from time import time
import io
import json
import pandas as pd

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

        if i == 1:
            with io.open('clf_params.txt', 'a') as outfile:

                params = results['params'][candidate]
                for param in params:
                    outfile.write("{0}={1}\n".format(param, params[param]))


def search(X, y):

    clf = RandomForestClassifier(n_estimators=20)

    param_grid = {"max_depth": [3, None],
                  "max_features": [1, 3, 4],
                  "min_samples_split": [2, 3, 4],
                  "min_samples_leaf": [1, 3, 4],
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}

    grid_search = GridSearchCV(clf, param_grid=param_grid)
    start = time()
    grid_search.fit(X, y)

    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.cv_results_['params'])))
    report(grid_search.cv_results_)


# Partie test

iris = load_iris()
X, y = iris.data, iris.target

nb_features = len(pd.DataFrame(X).columns)
with io.open('clf_params.txt', 'w') as outfile:
    outfile.write('nb_features={0}\n'.format(nb_features))

search(X, y)





