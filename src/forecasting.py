import pandas as pd

def predict_sales(df):

    forecast = (
        df.groupby('InvoiceDate')['TotalPrice']
        .sum()
        .tail(10)
    )

    return forecast