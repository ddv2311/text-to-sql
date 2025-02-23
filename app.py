from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load text-to-SQL model
MODEL_NAME = "tscholak/cxmefzzi"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to("cpu")  # Use 'cuda' if available

# Define table structure (to improve accuracy)
SCHEMA_INFO = """
Tables: employees(id, name, department, salary)
"""

def generate_sql(query):
    """Generate SQL query from natural language."""
    prompt = f"""
    {SCHEMA_INFO}
    Translate the following natural language query into an SQL statement:
    English: {query}
    SQL:
    """
    
    inputs = tokenizer(
        prompt.strip(),
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=256,
            num_beams=5,  # More beams for better accuracy
            early_stopping=True
        )

    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-processing to ensure correctness
    if "SELECT" not in sql_query.upper():
        sql_query = f"SELECT * FROM employees WHERE {sql_query}"

    return sql_query

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("query")

        if not query or not query.strip():
            return jsonify({"error": "Please provide a valid question."}), 400

        try:
            sql_query = generate_sql(query.strip())
            logging.info(f"Generated SQL: {sql_query}")
            return jsonify({"sql_query": sql_query})

        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return jsonify({"error": "An error occurred while processing your request."}), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
