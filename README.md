# 🚀 Text-to-SQL Converter 

## 📌 Overview
This project converts natural language queries into **SQL statements** finetuning a **pretrained NLP model**. It utilizes **Flask** for the API backend and a **Transformer-based model** (`t5-small`) for SQL generation.

## ✨ Features
- ✅ **Accurate SQL Generation** with schema-awareness.
- ✅ **Optimized** (loads model once normally then uses caching).

---
## Disclaimer
This might take 3-4 min as it loads and then converts the query so model might take some more time than expected.

## ⚡ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/ddv2311/text-to-sql.git
cd text-to-sql
```
### 2️⃣ Install Dependencies
```sh
pip install flask torch transformers gunicorn
```

### 3️⃣ Run the Jupyter Notebook to Use the Model

Run the provided Jupyter Notebook (texttosql.ipynb) to download and set up the model. This ensures that users run the model correctly before deploying the Flask app.

Steps:
```sh
jupyter notebook texttosql.ipynb
```
Run all cells to load and cache the model.
After running, the model will be ready for use in the Flask API.

### 🚀 Running the Application

1️⃣ Local Development
```sh
python app.py
```

### 🛠️ Troubleshooting

1️⃣ Slow Response Times?

Use Gunicorn instead of running Flask directly.

Ensure the model is cached locally (./model_cache).

2️⃣ Incorrect SQL Output?

The model does not know your schema unless provided.

Modify SCHEMA_INFO in app.py to reflect your database structure.

3️⃣ Want Cloud Deployment?

Render: Supports Flask/Gunicorn easily.

AWS/GCP/Azure: Use Docker for containerized deployment.

