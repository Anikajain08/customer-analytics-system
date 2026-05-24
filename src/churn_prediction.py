import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

churn_model = joblib.load(os.path.join(BASE_DIR, 'models', 'churn_model.pkl'))

import pandas as pd

def predict_churn(rfm):
    # define churn based on recency
    rfm['Churn'] = rfm['Recency'].apply(lambda x: 1 if x > 90 else 0)
    return rfm