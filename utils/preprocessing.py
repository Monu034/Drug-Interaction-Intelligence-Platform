"""
Utility functions for text preprocessing.
"""
import re

def clean_text(text):
    """Remove special characters and normalize whitespace."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^a-zA-Z0-9\s\-\.,]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_drug_name(name):
    """Uppercase and strip a drug name."""
    if not isinstance(name, str):
        return ""
    return name.strip().upper()
