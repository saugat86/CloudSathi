import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset

def load_jsonl_dataset(path):
    with open(path) as f:
        data = [json.loads(line) for line in f]
    return Dataset.from_dict({"input": [d["input"] for d in data], "output": [d["output"] for d in data]})

def main():
    model_name = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    dataset = load_jsonl_dataset("../data/synthetic_cloud_costs.jsonl")

    def preprocess(batch):
        model_inputs = tokenizer(
            batch["input"],
            max_length=64,
            truncation=True,
            padding="max_length"
        )
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(
                batch["output"],
                max_length=32,
                truncation=True,
                padding="max_length"
            )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    dataset = dataset.map(preprocess, batched=True, remove_columns=dataset.column_names)

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

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
        data_collator=data_collator,
    )
    trainer.train()
    model.save_pretrained("../model")
    tokenizer.save_pretrained("../model")

    # Optionally push to Hugging Face Hub
    if os.getenv("HF_TOKEN"):
        model.push_to_hub("CloudSathi-T5-Recommender", use_auth_token=True)
        tokenizer.push_to_hub("CloudSathi-T5-Recommender", use_auth_token=True)

if __name__ == "__main__":
    main()
