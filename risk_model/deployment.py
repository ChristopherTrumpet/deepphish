import pandas as pd
import numpy as np

import xgboost as xgb

labels = {0:"low", 1:"medium", 2:"high"}

def predict(name, literacy_score, seniority, degree_type, gender, department_hr, department_engineering, age):

    classifier = xgb.XGBClassifier()

    regressor = xgb.XGBRegressor()

    classifier.load_model("/Users/chris/Development/hack/deepphish/risk_model/model_classifier.json")

    regressor.load_model("/Users/chris/Development/hack/deepphish/risk_model/model_regressor.json")

    X = np.array([literacy_score, seniority, degree_type, gender, department_hr, department_engineering, age]).reshape((1, 7))

    classifier_prediciton = classifier.predict(X)
    regressor_prediction = regressor.predict(X)

    classification = classifier_prediciton[0]
    risk_value = regressor_prediction[0]

    str_classification = labels[classification]

    return name, str_classification, risk_value
