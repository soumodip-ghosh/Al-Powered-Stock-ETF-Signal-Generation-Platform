import requests

response = requests.post("http://127.0.0.1:8000/run-pipeline")
response.raise_for_status()

# 🔥 Safe to read parquet now
import pandas as pd
df = pd.read_parquet("data/clean_market.parquet")
print(df.head())