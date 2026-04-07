"""
Simple RAG (Retrieval-Augmented Generation) module.
Retrieves relevant context from the merged dataset before passing to LLM.
"""
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'merged_dataset.csv')

def retrieve_context(drug_a, drug_b, top_k=3):
    """
    Search the merged dataset for text relevant to the given drug pair.
    Returns a combined string of the top_k matching texts.
    """
    if not os.path.exists(DATA_PATH):
        return "No dataset found for context retrieval."

    df = pd.read_csv(DATA_PATH)
    d_a, d_b = drug_a.upper(), drug_b.upper()

    # Exact pair match
    mask = (
        ((df['drug_a'].str.upper() == d_a) & (df['drug_b'].str.upper() == d_b)) |
        ((df['drug_a'].str.upper() == d_b) & (df['drug_b'].str.upper() == d_a))
    )
    matches = df[mask]

    if matches.empty:
        # Fallback: partial match on either drug
        mask_partial = (
            df['drug_a'].str.upper().str.contains(d_a, na=False) |
            df['drug_b'].str.upper().str.contains(d_a, na=False) |
            df['drug_a'].str.upper().str.contains(d_b, na=False) |
            df['drug_b'].str.upper().str.contains(d_b, na=False)
        )
        matches = df[mask_partial]

    if matches.empty:
        return "No relevant context found in the dataset for this drug pair."

    texts = matches['text'].fillna('').head(top_k).tolist()
    return " ".join(texts)
