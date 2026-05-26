import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_products(df, customer_id):

    # filter customer data
    customer_data = df[df['CustomerID'] == customer_id]

    if customer_data.empty:
        return ["No data found for this customer"]

    # get top products
    top_products = (
        customer_data.groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    return list(top_products.index)