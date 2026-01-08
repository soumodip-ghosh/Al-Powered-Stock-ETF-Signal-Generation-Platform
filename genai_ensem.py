import pandas as pd
import joblib
import uvicorn
import ollama
import yfinance as yf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Infosys Stock Ensemble API")

# --- 1. THE SOURCE: DEFINING THE JSON FIELDS ---
# These are the fields FastAPI will ask for on the website (/docs)
class MarketData(BaseModel):
    Close: float
    RSI: float
    EMA12: float
    MA20: float
    MACD: float
    BB_width: float

# --- 2. LOAD MODELS ---
try:
    rf_model = joblib.load("rf_model.pkl")
    xgb_model = joblib.load("xgb_model.pkl")
    print("✅ Models loaded successfully.")
except Exception as e:
    print(f"❌ Load Error: {e}. Ensure rf_model.pkl and xgb_model.pkl are in C:\\Infosys")

# --- 3. FIX THE 404 ERROR (ROOT ROUTE) ---
@app.get("/")
def home():
    return {
        "message": "Welcome to Infosys GenAI Stock System",
        "instructions": "Go to /docs to use the interactive API"
    }

# --- 4. THE PREDICTION ENDPOINT ---
@app.post("/generate-signal/{ticker}")
def generate_signal(ticker: str, data: MarketData):
    try:
        # --- MATCHING: TRANSFORMING YOUR 6 JSON INPUTS TO THE 5 MODEL FEATURES ---
        # Feature 1: Daily_Return (Set to 0.001 as a placeholder for manual entry)
        daily_return = 0.001 
        
        # Feature 2: Volatility (Mapped from BB_width)
        volatility = data.BB_width 
        
        # Feature 3: SMA_ratio (Close / MA20)
        sma_ratio = data.Close / data.MA20 if data.MA20 != 0 else 1.0
        
        # Feature 4: EMA_ratio (Close / EMA12)
        ema_ratio = data.Close / data.EMA12 if data.EMA12 != 0 else 1.0
        
        # Feature 5: MACD (Direct pass)
        macd_val = data.MACD
        # Improved placeholders based on actual inputs
        daily_return = (data.Close - data.MA20) / data.MA20  # Rough estimate of recent trend
        volatility = data.BB_width  # BB_width is a direct measure of volatility

        # --- DATA ALIGNMENT FOR SKLEARN ---
        # This creates the exact 5-column DataFrame the model expects
        input_df = pd.DataFrame([{
            "Daily_Return": daily_return,
            "Volatility": volatility,
            "SMA_ratio": sma_ratio,
            "EMA_ratio": ema_ratio,
            "MACD": macd_val
        }])

        # Prediction
        rf_pred = float(rf_model.predict(input_df)[0])
        xgb_pred = float(xgb_model.predict(input_df)[0])
        avg_score = (rf_pred + xgb_pred) / 2

        # Decision Logic
        signal = "BUY" if avg_score > 0 else "SELL"

        # GenAI Explanation
        try:
            prompt = f"Stock {ticker} Signal: {signal}. RSI: {data.RSI}. Explain in 1 sentence."
            response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
            ai_msg = response['message']['content'].strip()
        except:
            ai_msg = "ML prediction successful. GenAI explanation currently offline."

        return {
            "ticker": ticker,
            "signal": signal,
            "prediction_score": round(avg_score, 6),
            "ai_analysis": ai_msg,
            "debug_features": input_df.to_dict(orient='records')[0]
        }

    except Exception as e:
        print(f"Prediction Crash: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
