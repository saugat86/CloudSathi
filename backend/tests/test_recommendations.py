import pytest
from fastapi.testclient import TestClient
from app.main import app

import torch

client = TestClient(app)

def test_recommendation_success(monkeypatch):
    # Patch model and tokenizer to avoid loading the real model
    class DummyModel:
        device = "cpu"
        def generate(self, **kwargs):
            return torch.tensor([[0, 1, 2]])
    class DummyTokenizer:
        def __call__(self, texts, **kwargs):
            return {"input_ids": torch.tensor([[1,2,3]]), "attention_mask": torch.tensor([[1,1,1]])}
        def decode(self, ids, skip_special_tokens=True):
            return "Use reserved instances for EC2"
    import app.api.recommendation_routes as rec_mod
    monkeypatch.setattr(rec_mod, "model", DummyModel())
    monkeypatch.setattr(rec_mod, "tokenizer", DummyTokenizer())
    monkeypatch.setattr(rec_mod, "device", "cpu")

    payload = {"cost_data": {"EC2": "high usage", "S3": "infrequent access"}}
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    assert "recommendation" in response.json()
    assert response.json()["recommendation"] == "Use reserved instances for EC2"

def test_recommendation_model_not_loaded(monkeypatch):
    import app.api.recommendation_routes as rec_mod
    monkeypatch.setattr(rec_mod, "model", None)
    monkeypatch.setattr(rec_mod, "tokenizer", None)
    payload = {"cost_data": {"EC2": "high usage"}}
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Recommendation model not loaded."

def test_recommendation_inference_error(monkeypatch):
    class DummyModel:
        device = "cpu"
        def generate(self, **kwargs):
            raise RuntimeError("inference failed")
    class DummyTokenizer:
        def __call__(self, texts, **kwargs):
            return {"input_ids": torch.tensor([[1,2,3]]), "attention_mask": torch.tensor([[1,1,1]])}
        def decode(self, ids, skip_special_tokens=True):
            return ""
    import app.api.recommendation_routes as rec_mod
    monkeypatch.setattr(rec_mod, "model", DummyModel())
    monkeypatch.setattr(rec_mod, "tokenizer", DummyTokenizer())
    monkeypatch.setattr(rec_mod, "device", "cpu")
    payload = {"cost_data": {"EC2": "high usage"}}
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate recommendation."
