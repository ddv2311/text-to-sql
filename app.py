from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

MODEL_NAME = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to("cpu")

SCHEMA_INFO = """
Tables: employees(id, name, salary)
"""

def generate_sql(query):
    prompt = f"translate English to SQL: {query} | Tables: {SCHEMA_INFO}"
    
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=256,
        truncation=True,
        padding="max_length"
    )

    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=128,
            num_beams=3,
            early_stopping=True
       
