import torch
from transformers import EncoderDecoderModel, DistilBertTokenizerFast

def load_recommender(model_dir="nlp/model"):
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)
    model = EncoderDecoderModel.from_pretrained(model_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    return model, tokenizer, device

def generate_recommendation(cost_data_json, model_dir="nlp/model"):
    model, tokenizer, device = load_recommender(model_dir)
    # Assume cost_data_json is a dict or str
    if isinstance(cost_data_json, dict):
        input_text = ", ".join(f"{k}: {v}" for k, v in cost_data_json.items())
    else:
        input_text = str(cost_data_json)
    inputs = tokenizer([input_text], return_tensors="pt", padding=True, truncation=True, max_length=64).to(device)
    summary_ids = model.generate(**inputs, max_length=32)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
