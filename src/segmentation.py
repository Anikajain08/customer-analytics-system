import pandas as pd
import joblib

# load model and scaler
import os
import joblib

# get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# correct paths
kmeans = joblib.load(os.path.join(BASE_DIR, 'models', 'kmeans_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'models', 'scaler.pkl'))

def segment_customers(df):
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    snapshot_date = df['InvoiceDate'].max()

    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    # scale
    rfm_scaled = scaler.transform(rfm)

    # predict
    rfm['Cluster'] = kmeans.predict(rfm_scaled)

    return rfm