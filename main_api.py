import yfinance as yf
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# ---------------- FEATURE ENGINEERING ----------------
def create_features(df):
    df["Daily_Return"] = df["Close"].pct_change()
    df["Volatility"] = df["Daily_Return"].rolling(14).std()

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    df["SMA_ratio"] = df["Close"] / df["SMA20"]
    df["EMA_ratio"] = df["Close"] / df["EMA20"]

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26

    df["Target"] = df["Close"].shift(-1)
    df.dropna(inplace=True)
    return df

# ---------------- TRAIN ----------------
def train_models():
    df = yf.download("AAPL", period="2y", auto_adjust=True)
    df.reset_index(inplace=True)
    data = create_features(df)

    FEATURES = ["Daily_Return", "Volatility", "SMA_ratio", "EMA_ratio", "MACD"]
    X = data[FEATURES]
    y = data["Target"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)

    xgb = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        objective="reg:squarederror"
    )
    xgb.fit(X_train, y_train)

    return rf, xgb

# ---------------- SAVE ----------------
rf_model, xgb_model = train_models()

with open("rf_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)

with open("xgb_model.pkl", "wb") as f:
    pickle.dump(xgb_model, f)

print("✅ Models saved as pickle files")
