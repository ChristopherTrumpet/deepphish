from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer

import pandas as pd
import numpy as np

import xgboost as xgb

df = pd.read_csv("data.csv")

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

labels = {1:"Risk", 0:"No-Risk"}

y = np.where(y > 0.5, 1, 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=94)

X_train, X_test, y_train, y_test = train_test_split(X, y)

# Use "hist" for constructing the trees, with early stopping enabled.
clf = xgb.XGBClassifier(tree_method="hist", early_stopping_rounds=2)
# Fit the model, test sets are used for early stopping.
clf.fit(X_train, y_train, eval_set=[(X_test, y_test)])




