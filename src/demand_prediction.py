import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, 'models', 'demand_model.pkl'))

def predict_demand(day, month, year):
    data = pd.DataFrame([[day, month, year]], columns=['Day', 'Month', 'Year'])
    return model.predict(data)[0]