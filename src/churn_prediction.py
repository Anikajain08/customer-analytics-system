import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

churn_model = joblib.load(os.path.join(BASE_DIR, 'models', 'churn_model.pkl'))

# load model
churn_model = joblib.load('models/churn_model.pkl')

def predict_churn(rfm):
    X = rfm[['Recency', 'Frequency', 'Monetary']]
    rfm['Churn'] = churn_model.predict(X)
    return rfm