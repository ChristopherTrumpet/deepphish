from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

import xgboost as xgb

def train_model(): 
    def map_ranges(x):
        if 0 < x <= 0.333:
            return 0
        elif 0.333 < x <= 0.666:
            return 1
        else:
            return 2

    df = pd.read_csv("data.csv")

    df = df.drop("Unnamed: 0", axis=1)

    X = df.iloc[:, :-1]

    y = df.iloc[:, -1]

    y_classifier = y.map(map_ranges)

    X_train, X_test, y_train, y_test = train_test_split(X, y_classifier)

    # Use "hist" for constructing the trees, with early stopping enabled.
    clf = xgb.XGBClassifier(tree_method="hist")

    # Fit the model, test sets are used for early stopping.
    clf.fit(X_train, y_train, eval_set=[(X_test, y_test)])

    clf.save_model("model_classifier.json")

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    clf_regressor = xgb.XGBRegressor()

    clf_regressor.fit(X_train, y_train, eval_set=[(X_test, y_test)])

    clf_regressor.save_model("model_regressor.json")

train_model()





