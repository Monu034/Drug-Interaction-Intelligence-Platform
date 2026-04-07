# ML ENGINE: Core Inference Logic for Drug Interaction Prediction
import pickle
import os
import pandas as pd

# Necessary for unpickling new-style wrapper objects
from ml.model_wrapper import PredictionWrapper

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'saved_model.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), '../final_dataset.csv')

_model = None
_dataset = None

def load_data():
    global _dataset
    if _dataset is None and os.path.exists(DATA_PATH):
        _dataset = pd.read_csv(DATA_PATH, keep_default_na=False)
    return _dataset

def load_model():
    global _model
    global MODEL_PATH
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            alt_path = os.path.abspath(os.path.join(os.getcwd(), 'ml', 'saved_model.pkl'))
            if os.path.exists(alt_path):
                MODEL_PATH = alt_path
            else:
                raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
                
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
    return _model

def predict_interaction(drug_a, drug_b):
    model = load_model()
    # Normalize input order
    drugs = sorted([str(drug_a).upper(), str(drug_b).upper()])
    feature = " ".join(drugs)
    
    # 1. Check Exact Matches First (Golden standard for known data)
    df = load_data()
    context = ""
    exact_match_found = False
    prediction = None

    if df is not None:
        mask = (
            ((df['drug_a'].str.upper() == drugs[0]) & (df['drug_b'].str.upper() == drugs[1])) |
            ((df['drug_a'].str.upper() == drugs[1]) & (df['drug_b'].str.upper() == drugs[0]))
        )
        matches = df[mask]
        if not matches.empty:
            exact_match_found = True
            prediction = str(matches['severity'].iloc[0])
            context = " ".join(matches['description'].fillna('').head(3).tolist())
            
    # 2. Fallback to the AI Model (Logistic Reg / Random Forest / XGBoost based on winner)
    if not exact_match_found:
        res = model.predict([feature])
        prediction = str(res[0])
        context = "Reference context unavailable for this exact pair."
        
    return prediction, context
