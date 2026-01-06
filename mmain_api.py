from fastapi import FastAPI, HTTPException
import pickle

app = FastAPI()

# Helper function to load the master data
def load_master_data():
    try:
        with open("master_rf_results.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

@app.get("/")
def home():
    return {"status": "Online", "engine": "RandomForest_XGBoost_Ensemble"}

@app.get("/signal/{ticker}")
def get_signal(ticker: str):
    data = load_master_data()
    if not data:
        raise HTTPException(status_code=500, detail="Master Pickle not found. Run Engine.")
    
    ticker_data = data.get(ticker.upper())
    if not ticker_data:
        raise HTTPException(status_code=404, detail=f"No data for {ticker}")

    # Logic for Recommendation
    pred = ticker_data["pred_return"]
    if pred > 0.005: rec = "BUY"
    elif pred < -0.005: rec = "SELL"
    else: rec = "HOLD"

    return {
        "ticker": ticker.upper(),
        "recommendation": rec,
        "metrics": ticker_data
    }