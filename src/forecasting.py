import pandas as pd

def predict_sales(df):
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    sales = df.groupby('InvoiceDate')['TotalPrice'].sum()

    return sales.tail(10)