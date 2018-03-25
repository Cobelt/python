from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

import pandas as pd
import numpy as np

np.random.seed(0)

iris = load_iris()

data = pd.DataFrame(iris.data, columns=iris.feature_names)

# iris.target = 0, 1 ou 2 / iris.target_names contient les noms
data['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
# random attribution of random data
data['is_train'] = np.random.uniform(0, 1, len(data)) <= .75

# ajoute toute la data d'entrainement dans le trainTab et le reste dans le testTab
trainTab = data[data['is_train']==True]
testTab = data[data['is_train']==False]
# print('qty of data from train:', len(trainTab))
# print('qty of data for test:', len(testTab))

features = data.columns[:4]
known = pd.factorize(trainTab['species'])[0]

# On doit récuperer les params
clf = RandomForestClassifier() # en ajoutant les bons params

clf.fit(trainTab[features], known)

# prediction
clf.predict(testTab[features])

predicts = iris.target_names[clf.predict(testTab[features])]

# print(predicts[0:5])
# print(testTab['species'].head())

# tableau a deux entrées pour afficher les erreurs
print(pd.crosstab(testTab['species'], predicts, rownames=['Actual Species'], colnames=['Predicted Species']).head())

# on affiche le poids de chaque features
print(list(zip(trainTab[features], clf.feature_importances_)))

