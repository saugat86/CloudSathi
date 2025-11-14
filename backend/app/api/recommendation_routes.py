"""API routes for cost recommendations."""
import os
import sys
import traceback
from typing import Any, Dict

import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_PATH = os.getenv("RECOMMENDER_MODEL_PATH", "../../nlp/model")


class RecommendationRequest(BaseModel):
    """Request model for recommendation endpoint."""

    cost_data: Dict[str, Any]


class RecommendationResponse(BaseModel):
    """Response model for recommendation endpoint."""

    recommendation: str


router = APIRouter()

# Load model and tokenizer once at startup
try:
    TOKENIZER = AutoTokenizer.from_pretrained(MODEL_PATH)
    MODEL = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    MODEL = MODEL.to(DEVICE)
except OSError as e:
    print(f"[ERROR] Failed to load recommendation model: {e}", file=sys.stderr)
    TOKENIZER = None
    MODEL = None
    DEVICE = None


def preprocess_cost_data(cost_data: Dict[str, Any]) -> str:
    """Preprocesses cost data into a string for the model."""
    # Simple preprocessing: extract high-cost services/resources
    # (You can improve this logic as needed)
    if not isinstance(cost_data, dict):
        return str(cost_data)
    items = []
    for k, v in cost_data.items():
        if isinstance(v, (int, float)) and v > 0:
            items.append(f"{k}: {v}")
        elif isinstance(v, str):
            items.append(f"{k}: {v}")
    return ", ".join(items)


@router.post("/recommendations", response_model=RecommendationResponse)
def get_recommendation(request: RecommendationRequest):
    """Generates a cost optimization recommendation."""
    if MODEL is None or TOKENIZER is None:
        raise HTTPException(
            status_code=500, detail="Recommendation model not loaded."
        )
    try:
        input_text = preprocess_cost_data(request.cost_data)
        inputs = TOKENIZER(
            [input_text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=64,
        )
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        summary_ids = MODEL.generate(**inputs, max_length=32)
        rec = TOKENIZER.decode(summary_ids[0], skip_special_tokens=True)
        return {"recommendation": rec}
    except Exception as exc:
        print(f"[ERROR] Model inference failed: {traceback.format_exc()}", file=sys.stderr)
        raise HTTPException(
            status_code=500, detail="Failed to generate recommendation."
        ) from exc
