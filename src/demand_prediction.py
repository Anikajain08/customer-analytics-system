import pandas as pd

def predict_demand(df):
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    demand = df.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False)
    return demand.head(10)