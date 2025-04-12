from faker import Faker 
import pandas as pd 
import numpy as np 
import random
from scipy.optimize import minimize

fake = Faker() 

def create_dummy_data(num_rows=10):
    data = []

    department = np.random.randint(1, 4, num_rows)
    degreetype = np.random.randint(0, 2, num_rows)

    

    gender = np.random.randint(0, 2, num_rows)

    lit_score = []

    for i in range(num_rows): 
        if degreetype[i] == 1: 
            score = random.normalvariate(70, 15)
            score = min(100, score)
            score = round(score)
            lit_score.append(score)
        else: 
            score = random.normalvariate(45, 15)
            score = min(100, score)
            score = round(score)
            lit_score.append(score)

    age = np.random.Generator.normal(np.random.default_rng(), loc=37, scale=25, size=num_rows)

    age = np.clip(age, 22, 80)

    age = np.round(age).astype(int)

    s = []

    for i in range(num_rows): 
        seniority = np.random.randint(0, 20, size=1)[0]

        problem = age[i] - seniority

        if problem < 22: 
            seniority -= (age[i] - problem)
        
        s.append(seniority)

    d = {"TechScore": lit_score, "Seniority": s, "Department": department, "Gender": gender, "DegreeType": degreetype, "Age": age}

    df = pd.DataFrame(d)

    return df

def one_hot_encode(df): 
    # One-hot encode the column
    dep_dic = {1:"Engineering", 2: "HR", 3: "IT"}

    df["Department"] = df["Department"].map(dep_dic)

    df_encoded = pd.get_dummies(df, columns=['Department'], drop_first=True)

    return df_encoded

def find_betas(data): 

    init_betas = np.zeros(7)

    def logit(betas, x):
         y = np.dot(betas, x)
         p = (1 / (1 + np.exp(-y)))**0.5
         return p

    def mse(betas): 
        return np.sum((0.5 - logit(betas, data)))**2

    result = minimize(mse, x0 = init_betas)

    return result.x

#hr =  create_dummy_data(200) 

def logistic_regression(betas, data): 
    y = 0
    
    for i in range(len(betas)):
        y += betas[i] * data[i]
    
    p = (1 / (1 + np.exp(-y)))**0.2

    return p




def construct_complete_dataframe(num_rows=10): 

    betas = [-0.3, 0.1, -0.5, -0.5, 0.3, -0.75, 0.5]

    df = create_dummy_data(num_rows)

    df = one_hot_encode(df)

    df = df.astype(int)

    df = df.T

    p_values = []

    for col in df: 
        p = logistic_regression(betas, df[col])
        p_values.append(p)

    df = df.T

    df["Risk"] = p_values

    return df


sample_data = construct_complete_dataframe(10000)

sample_data.to_csv("data.csv")








