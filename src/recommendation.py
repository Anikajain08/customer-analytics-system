import pandas as pd
from pathlib import Path

# load data (paths resolved relative to project root)
BASE_DIR = Path(__file__).resolve().parents[1]
data_dir = BASE_DIR / 'data'

customer_product_path = data_dir / 'customer_product_matrix.csv'
similarity_path = data_dir / 'similarity_matrix.csv'

if not customer_product_path.exists():
    raise FileNotFoundError(f"customer_product_matrix.csv not found at {customer_product_path}")
if not similarity_path.exists():
    raise FileNotFoundError(f"similarity_matrix.csv not found at {similarity_path}")

customer_product = pd.read_csv(customer_product_path, index_col=0)
similarity_df = pd.read_csv(similarity_path, index_col=0)

# convert index/columns to int (handles float-like strings like '12346.0')
try:
    customer_product.index = pd.to_numeric(customer_product.index, errors='raise').astype(int)
    similarity_df.index = pd.to_numeric(similarity_df.index, errors='raise').astype(int)
    similarity_df.columns = pd.to_numeric(similarity_df.columns, errors='raise').astype(int)
except Exception as e:
    raise ValueError(f"Failed to convert index/columns to int: {e}")

def recommend_products(customer_id, top_n=5):
    try:
        customer_id = int(customer_id)

        if customer_id not in similarity_df.index:
            return f"Customer ID {customer_id} not found"

        # find similar customers
        similar_customers = similarity_df.loc[customer_id].sort_values(ascending=False)[1:6]
        similar_ids = similar_customers.index

        # get recommendations
        recommended_products = customer_product.loc[similar_ids].sum().sort_values(ascending=False)

        return recommended_products.head(top_n)

    except Exception as e:
        return f"Error: {e}"