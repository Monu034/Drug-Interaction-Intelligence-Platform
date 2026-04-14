# BACKEND: Route Handlers and Controller Logic
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import os
from ml.predict import predict_interaction
from genai.llm import generate_explanation
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db
from db import models

router = APIRouter()
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    history = db.query(models.InteractionHistory).order_by(models.InteractionHistory.timestamp.desc()).limit(10).all()
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request,
        "history": history
    })

@router.get("/api/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(models.InteractionHistory).order_by(models.InteractionHistory.timestamp.desc()).limit(10).all()
    return {"history": history}

@router.post("/api/predict")
async def api_predict(
    request: Request,
    drug_a: str = Form(...),
    drug_b: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        from utils.drug_info import get_drug_details
        severity, context = predict_interaction(drug_a, drug_b, db=db)
        
        # Get metadata for the drugs
        details_a = get_drug_details(drug_a)
        details_b = get_drug_details(drug_b)
        
        # Save to database
        db_history = models.InteractionHistory(
            drug_a=drug_a.upper(),
            drug_b=drug_b.upper(),
            severity=severity
        )
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        
        return {
            "severity": severity,
            "drug_a_info": details_a,
            "drug_b_info": details_b,
            "context": context,
            "id": db_history.id # Return ID so we can update explanation later if needed
        }
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 400

from fastapi.responses import StreamingResponse
from genai.llm import generate_explanation_stream
import json

@router.get("/api/explain/stream")
async def stream_explanation(
    drug_a: str,
    drug_b: str,
    severity: str,
    context: str = ""
):
    async def event_generator():
        # First check for mock data locally to avoid latency
        from genai.llm import get_mock_explanation
        mock = get_mock_explanation(drug_a, drug_b)
        
        if mock:
            # Simulate streaming for mock data to keep the UI consistent
            words = mock.split()
            for i in range(0, len(words), 3):
                chunk = " ".join(words[i:i+3]) + " "
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                import asyncio
                await asyncio.sleep(0.05)
            yield "data: [DONE]\n\n"
        else:
            # Real streaming from Gemini
            async for chunk in generate_explanation_stream(drug_a, drug_b, severity, context):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/predict")
async def get_predict_fallback():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/")

@router.post("/predict")
async def get_prediction(
    request: Request,
    drug_a: str = Form(...),
    drug_b: str = Form(...)
):
    # FALLBACK for non-JS users (traditional form submission)
    from db.database import SessionLocal
    db = SessionLocal()
    try:
        severity, context = predict_interaction(drug_a, drug_b, db=db)
    except Exception as e:
        db.close()
        return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "error": str(e)})
    finally:
        db.close()

    # Note: Traditional form doesn't do streaming easily without page reload
    # This route stays for compatibility but we encourage Fetch/SSE
    from genai.llm import generate_explanation
    llm_result = generate_explanation(drug_a, drug_b, severity, context)
    
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request,
        "drug_a": drug_a.upper(),
        "drug_b": drug_b.upper(),
        "severity": severity,
        "explanation": llm_result.get("explanation"),
        "scroll_to_results": True
    })
