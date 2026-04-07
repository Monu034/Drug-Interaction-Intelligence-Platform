# BACKEND: Route Handlers and Controller Logic
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import os
from ml.predict import predict_interaction
from genai.llm import generate_explanation

router = APIRouter()
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@router.post("/predict")
async def get_prediction(
    request: Request,
    drug_a: str = Form(...),
    drug_b: str = Form(...)
):
    # 1. ML Prediction
    try:
        severity, context = predict_interaction(drug_a, drug_b)
    except FileNotFoundError:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "request": request,
            "error": "Model not trained. Please run 'python -m ml.train' and restart the server.",
            "drug_a": drug_a,
            "drug_b": drug_b
        })
    except Exception as e:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "request": request,
            "error": str(e),
            "drug_a": drug_a,
            "drug_b": drug_b
        })
        
    # 2. LLM Explanation
    llm_result = generate_explanation(drug_a, drug_b, severity, context)
    
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request,
        "drug_a": drug_a.upper(),
        "drug_b": drug_b.upper(),
        "severity": severity,
        "explanation": llm_result.get("explanation"),
        "risk": llm_result.get("risk"),
        "scroll_to_results": True
    })
