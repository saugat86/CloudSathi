import os
from transformers import AutoTokenizer

MODEL_PATH = "../../nlp/model"
try:
    print(f"Loading from {MODEL_PATH}")
    TOKENIZER = AutoTokenizer.from_pretrained(MODEL_PATH)
    print("Success")
except Exception as e:
    print(f"Caught exception: {type(e).__name__}: {e}")
