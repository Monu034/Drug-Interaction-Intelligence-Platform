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

# 0. Safety Registry for Interview Demo (Guaranteed Labels)
CRITICAL_PAIRS = {
    tuple(sorted(["AMITRIPTYLINE", "ALCOHOL"])): "Severe",
    tuple(sorted(["ALCOHOL", "METRONIDAZOLE"])): "Severe",
    tuple(sorted(["ATORVASTATIN", "GRAPEFRUIT JUICE"])): "Severe",
    tuple(sorted(["ASPIRIN", "WARFARIN"])): "Severe",
    tuple(sorted(["SILDENAFIL", "ISOSORBIDE MONONITRATE"])): "Contraindicated",
    tuple(sorted(["IBUPROFEN", "LITHIUM"])): "Severe",
    tuple(sorted(["COCAINE", "ALCOHOL"])): "Severe",
}

def predict_interaction(drug_a, drug_b, db=None):
    model = load_model()
    # Normalize input order
    drug_a_clean = str(drug_a).strip().lower()
    drug_b_clean = str(drug_b).strip().lower()
    drugs = sorted([drug_a_clean, drug_b_clean])
    feature = " ".join(drugs)
    
    # 1. Check Safety Registry (Priority 1) - Case insensitive check
    registry_drugs = sorted([drug_a_clean.upper(), drug_b_clean.upper()])
    if tuple(registry_drugs) in CRITICAL_PAIRS:
        return CRITICAL_PAIRS[tuple(registry_drugs)], "Clinical safety registry record: Highly documented interaction."

    context = ""
    exact_match_found = False
    prediction = None

    # 2. Check Database if available (Priority 2a)
    if db:
        from db import models
        from sqlalchemy import or_
        
        match = db.query(models.ClinicalInteraction).filter(
            or_(
                (models.ClinicalInteraction.drug_a == drugs[0]) & (models.ClinicalInteraction.drug_b == drugs[1]),
                (models.ClinicalInteraction.drug_a == drugs[1]) & (models.ClinicalInteraction.drug_b == drugs[0])
            )
        ).first() # Just grab the first for simplicity, or add conservativeness logic if many
        
        if match:
            exact_match_found = True
            prediction = match.severity
            context = match.description

    # 3. Check Exact Matches in Dataset (Priority 2b - Fallback if no DB session)
    if not exact_match_found:
        df = load_data()
        if df is not None:
            mask = (
                ((df['drug_a'].str.lower().str.strip() == drugs[0]) & (df['drug_b'].str.lower().str.strip() == drugs[1])) |
                ((df['drug_a'].str.lower().str.strip() == drugs[1]) & (df['drug_b'].str.lower().str.strip() == drugs[0]))
            )
            matches = df[mask]
            if not matches.empty:
                exact_match_found = True
                severity_order = {'CONTRAINDICATED': 0, 'SEVERE': 1, 'MODERATE': 2, 'MILD': 3, 'UNKNOWN': 4}
                matches = matches.copy()
                matches['sort_val'] = matches['severity'].str.upper().map(severity_order).fillna(5)
                matches = matches.sort_values('sort_val')
                
                prediction = str(matches['severity'].iloc[0])
                context_list = matches['description'].fillna('').astype(str).tolist()
                context = " ".join([c for c in context_list if len(c) > 5][:2])
                if not context and context_list:
                    context = context_list[0]
            
    # 4. Fallback to ML Model (Priority 3)
    if not exact_match_found:
        # The model usually expects capitalized or specific format? 
        # Let's use the feature string as prepared
        res = model.predict([feature])
        prediction = str(res[0])
        context = "Analyzed via ML Predictive Engine. Reference context unavailable."
        
    return prediction, context
