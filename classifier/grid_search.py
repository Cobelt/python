import numpy as np

from time import time
import io

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
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

        if i == 1:
            with io.open('clf_params.json', 'a') as outfile:
                outfile.write("Parameters = {0}".format(results['params'][candidate]))


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


iris = load_iris()
X, y = iris.data, iris.target
search(X, y)





