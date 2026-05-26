# load model and scaler
import os

# get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# correct paths
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def segment_customers(df):
    import pandas as pd

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (x.max() - x.min()).days,
        'InvoiceNo': 'count',
        'TotalPrice': 'sum'
    }).reset_index()

    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    # 🔥 GUARANTEED SEGMENT COLUMN
    rfm['Segment'] = pd.qcut(
        rfm['Monetary'],
        q=3,
        labels=['Low Value', 'Medium Value', 'High Value']
    )

    return rfm