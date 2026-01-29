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
# Resolve to absolute path to avoid HFValidationError with relative paths
if not os.path.isabs(MODEL_PATH):
    MODEL_PATH = os.path.abspath(MODEL_PATH)


class RecommendationRequest(BaseModel):
    """Request model for recommendation endpoint."""

    cost_data: Dict[str, Any]


class RecommendationResponse(BaseModel):
    """Response model for recommendation endpoint."""

    recommendation: str


router = APIRouter()

# Load model and tokenizer once at startup
try:
    if os.path.exists(MODEL_PATH) and os.listdir(MODEL_PATH):
         TOKENIZER = AutoTokenizer.from_pretrained(MODEL_PATH)
         MODEL = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
         DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
         MODEL = MODEL.to(DEVICE)
    else:
         print(f"[WARNING] Model directory {MODEL_PATH} not found or empty. Skipping model load.", file=sys.stderr)
         TOKENIZER = None
         MODEL = None
         DEVICE = None
except Exception as e:
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
    # Check if mock data is enabled
    use_mock_data = os.getenv('USE_MOCK_DATA', 'false').lower() == 'true'

    if MODEL is None or TOKENIZER is None:
        if use_mock_data:
            # Return mock recommendation when model is not loaded
            input_text = preprocess_cost_data(request.cost_data)
            mock_recommendations = [
                "Consider using Reserved Instances for EC2 to save up to 75% on compute costs.",
                "Switch to spot instances for non-critical workloads to reduce costs by 70-90%.",
                "Move infrequently accessed S3 data to Glacier storage class for 80% savings.",
                "Right-size your RDS instances based on actual usage patterns.",
                "Enable auto-scaling to optimize resource utilization and reduce costs."
            ]
            # Simple mock logic based on input
            if "ec2" in input_text.lower() or "compute" in input_text.lower():
                return {"recommendation": mock_recommendations[0]}
            elif "s3" in input_text.lower() or "storage" in input_text.lower():
                return {"recommendation": mock_recommendations[2]}
            elif "rds" in input_text.lower() or "database" in input_text.lower():
                return {"recommendation": mock_recommendations[3]}
            else:
                return {"recommendation": mock_recommendations[4]}
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
