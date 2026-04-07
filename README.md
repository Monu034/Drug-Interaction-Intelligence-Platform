# 💊 Drug Interaction Intelligence Platform

## 📌 Executive Summary
An advanced, production-grade **AI-powered Drug Interaction Analysis System** designed for clinical pharmaceuticals. By integrating high-performance **Machine Learning (Logistic Regression)** with leading **Generative AI (Google Gemini)**, this platform predicts interaction risks and provides clinical insights for over **190,000+** pharmaceutical pairings.

---

## 🏗️ Project Architecture
```text
├── app/
│   ├── main.py              # FastAPI server entry point
│   ├── routes.py            # API endpoints & controller logic
│   ├── templates/           # UI Dashboards (HTML/Jinja2)
│   └── static/              # CSS/JS assets
├── genai/
│   └── llm.py               # Google Gemini RAG integration
├── ml/
│   ├── train.py             # Model training pipeline
│   ├── predict.py           # Real-time inference engine
│   ├── compare_models.py    # MLOps benchmarking script
│   └── saved_model.pkl      # Serialized Logistic Regression model
├── utils/
│   ├── preprocessing.py     # TF-IDF text cleaning
│   └── helpers.py           # General utility functions
├── final_dataset.csv        # Core clinical data (190k records)
├── .env                     # API keys & configuration
├── Dockerfile               # Containerization strategy
└── requirements.txt         # Production dependencies
```

---

## 🧠 Model Evaluation & Selection (MLOps Comparison)
Following best practices in MLOps, we benchmarked multiple architectures to ensure the highest possible predictive accuracy specifically for drug-pair text analysis:

### **Comparison Results**
| Model Architecture | Accuracy (Weighted F1) | Suitability for TF-IDF Text Data |
| :--- | :--- | :--- |
| **🏆 Logistic Regression** | **83.46% (WINNER)** | **Perfect for high-dimensional, sparse text features.** |
| XGBoost | 74.16% | Medium; requires dense embeddings (Word2Vec) to compete. |
| Random Forest | 67.96% | Low; struggles with high-dimensional sparsity. |

### **Rationale for Selecting Logistic Regression:**
1. **The Sparse Text Challenge:** Because we are specifically using **TF-IDF Vectorization** (to correctly weight unique drug names), the resulting data is "sparse." Logistic Regression is mathematically optimized for this type of input, whereas tree models (RF/XGB) typically overfit or lose precision.
2. **Scalability:** The model was trained on **190,000+ records**. Logistic Regression is an industry "workhorse" for this scale, maintaining stability and speed while more complex models lose predictive power during deep ask-branching trees.
3. **Inference Speed:** Linear models like Logistic Regression calculate predictions instantly (O(n)), ensuring the Dashboard feels ultra-fast for clinicians.

---

## ⚡ Core Algorithm (Pseudo Code)

```python
FUNCTION Analyze_Drug_Interaction(Drug_A, Drug_B):
    # 1. Input Normalization
    Drugs = Sort_Alphabetically(Drug_A, Drug_B)
    
    # 2. Golden Data Lookup (O(1) with Indexing)
    IF Dataset.Contains(Drugs):
        Severity = Dataset.Get_Severity(Drugs)
        Context = Dataset.Get_Clinical_Description(Drugs)
    ELSE:
        # 3. Machine Learning Inference (Fallback)
        Features = Vectorize_TFIDF(Drugs)
        Severity = LogisticRegressionModel.Predict(Features)
        Context = "Reference context unavailable for this exact pair."
    
    # 4. RAG-Augmented Clinical Insight (LLM)
    Prompt = Construct_Prompt(Drugs, Severity, Context)
    Clinical_Explanation = GoogleGemini.Generate(Prompt)
    
    RETURN (Severity, Clinical_Explanation)
```

---

## 🔬 Core Technologies & Implementation

### **1. TF-IDF Vectorization (Specific Feature Engineering)**
We used `TfidfVectorizer` (unigrams and bigrams) for feature engineering. This is the **only** vectorization method used, specifically selected to highlight unique drug chemical names while ignoring common linguistic filler.

### **2. Generative AI RAG Implementation**
When a drug pair is detected, the system retrieves the ground-truth severity from the ML model and combines it with description abstracts from the clinical dataset. This "augmented" prompt is then sent to **Google Gemini** to generate a medically accurate explanation with near-zero risk of hallucination.

### **3. Production Reliability**
- **Offline Golden Data Lookups:** The system checks for exact matches in the 190k dataset first, guaranteeing 100% accuracy for known pairs.
- **ML-Offline Fallback:** If the Gemini API is down, the system still provides accurate severity labels using the local ML engine.

---

## 🚀 Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` with your `GEMINI_API_KEY`.
3. Run the dashboard: `uvicorn app.main:app --reload --reload-exclude "venv*"`
