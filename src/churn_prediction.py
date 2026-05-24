def predict_churn(rfm):
    # simple rule-based churn (no model needed)
    rfm['Churn'] = rfm['Recency'].apply(lambda x: 1 if x > 90 else 0)
    return rfm