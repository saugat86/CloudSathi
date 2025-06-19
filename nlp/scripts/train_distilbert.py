import os
import json
import torch
from transformers import DistilBertTokenizerFast, EncoderDecoderModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load synthetic dataset
def load_jsonl_dataset(path):
    with open(path) as f:
        data = [json.loads(line) for line in f]
    return Dataset.from_dict({"input": [d["input"] for d in data], "output": [d["output"] for d in data]})

def load_recommender(model_dir="nlp/model"):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    return model, tokenizer, device

def generate_recommendation(cost_data_json, model_dir="nlp/model"):
    model, tokenizer, device = load_recommender(model_dir)
    if isinstance(cost_data_json, dict):
        input_text = ", ".join(f"{k}: {v}" for k, v in cost_data_json.items())
    else:
        input_text = str(cost_data_json)
    inputs = tokenizer([input_text], return_tensors="pt", padding=True, truncation=True, max_length=64).to(device)
    summary_ids = model.generate(**inputs, max_length=32)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def main():
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
    model = EncoderDecoderModel.from_encoder_decoder_pretrained(model_name, model_name)

    dataset = load_jsonl_dataset("../data/synthetic_cloud_costs.jsonl")
    def preprocess(batch):
        inputs = tokenizer(batch["input"], padding="max_length", truncation=True, max_length=64, return_tensors="pt")
        outputs = tokenizer(batch["output"], padding="max_length", truncation=True, max_length=32, return_tensors="pt")
        batch["input_ids"] = inputs.input_ids[0]
        batch["attention_mask"] = inputs.attention_mask[0]
        batch["labels"] = outputs.input_ids[0]
        return batch
    dataset = dataset.map(preprocess)

    training_args = TrainingArguments(
        output_dir="../model",
        per_device_train_batch_size=2,
        num_train_epochs=10,
        save_steps=10,
        save_total_limit=1,
        logging_steps=5,
        report_to=[],
        fp16=torch.cuda.is_available(),
        remove_unused_columns=False
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    trainer.train()
    model.save_pretrained("../model")
    tokenizer.save_pretrained("../model")

    # Optionally push to Hugging Face Hub
    if os.getenv("HF_TOKEN"):
        model.push_to_hub("CloudSathi-DistilBERT-Recommender", use_auth_token=True)
        tokenizer.push_to_hub("CloudSathi-DistilBERT-Recommender", use_auth_token=True)

if __name__ == "__main__":
    main()
