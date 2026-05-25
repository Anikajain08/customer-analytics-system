import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def recommend_products(df, customer_id, top_n=5):

    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # create customer-product matrix
    matrix = df.pivot_table(
        index='CustomerID',
        columns='StockCode',
        values='TotalPrice',
        aggfunc='sum',
        fill_value=0
    )

    # compute similarity
    similarity = cosine_similarity(matrix)
    similarity_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

    if customer_id not in similarity_df.index:
        return f"Customer ID {customer_id} not found"

    # find similar customers
    similar_users = similarity_df.loc[customer_id].sort_values(ascending=False)[1:6]
    similar_ids = similar_users.index

    # recommend products
    recommended = matrix.loc[similar_ids].sum().sort_values(ascending=False)

    return recommended.head(top_n)