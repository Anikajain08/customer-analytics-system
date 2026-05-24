import pandas as pd
import joblib

# load model and scaler
import os
import joblib

# get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# correct paths
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)

    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
    return rfm