import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import ta

#configurations
TICKER_FILE = "data/ticker.txt"

RAW_DATA_FILE = "data/raw_market_data.parquet"
CLEAN_DATA_FILE = "data/clean_market_data.parquet"
ENCODER_FILE = "data/ticker_encoder.parquet"

START_DATE = "2015-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")

os.makedirs("data", exist_ok=True)

#load tickers
def load_tickers(path):
    with open(path, "r") as f:
        tickers = [line.strip() for line in f if line.strip()]
    return sorted(set(tickers))


#fatch raw data from yfinance
def fetch_raw_data(tickers, start, end):
    df = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=False,
        threads=True
    )

    df = df.stack(level=0, future_stack=True).reset_index()
    df.columns = [c.lower() for c in df.columns]

    return df


#ticker encoder
def load_or_create_encoder(tickers):
    if os.path.exists(ENCODER_FILE):
        encoder = pd.read_parquet(ENCODER_FILE)
    else:
        encoder = pd.DataFrame({
            "ticker": tickers,
            "ticker_id": range(len(tickers))
        })
        encoder.to_parquet(ENCODER_FILE, index=False)

    return encoder


def encode_tickers(df, encoder):
    df = df.merge(encoder, on="ticker", how="left")

    if df["ticker_id"].isna().any():
        missing = df[df["ticker_id"].isna()]["ticker"].unique()
        raise ValueError(f"Missing ticker_id for: {missing}")

    return df

#feature engineering
def add_features(df):
    df = df.sort_values(["ticker", "date"])

    out = []

    for ticker, g in df.groupby("ticker"):
        g = g.copy()

        # Returns
        g["daily_return"] = g["close"].pct_change(fill_method=None)
        g["volume_change"] = g["volume"].pct_change(fill_method=None)

        # Moving Averages
        g["ma20"] = ta.trend.SMAIndicator(g["close"], window=20).sma_indicator()
        g["ma50"] = ta.trend.SMAIndicator(g["close"], window=50).sma_indicator()

        # Ratio
        g["close_ma20_ratio"] = g["close"] / g["ma20"]

        # Volatility (20-day std of returns)
        g["volatility"] = g["daily_return"].rolling(20).std()

        # RSI
        g["rsi"] = ta.momentum.RSIIndicator(
            close=g["close"], window=14
        ).rsi()

        # EMA
        g["ema12"] = ta.trend.EMAIndicator(
            close=g["close"], window=12
        ).ema_indicator()

        g["ema26"] = ta.trend.EMAIndicator(
            close=g["close"], window=26
        ).ema_indicator()

        # MACD
        macd = ta.trend.MACD(
            close=g["close"],
            window_fast=12,
            window_slow=26,
            window_sign=9
        )

        g["macd"] = macd.macd()
        g["macd_signal"] = macd.macd_signal()

        out.append(g)

    return pd.concat(out, ignore_index=True)


#cleanup bad index columns
def drop_bad_index_columns(df):
    bad_cols = ["__index_level_0__", "index", "level_0"]
    return df.drop(columns=[c for c in bad_cols if c in df.columns])


#main pipeline function
def run_pipeline():
    print("Loading tickers...")
    tickers = load_tickers(TICKER_FILE)

    print("Fetching raw data...")
    raw_df = fetch_raw_data(tickers, START_DATE, END_DATE)
    raw_df = drop_bad_index_columns(raw_df)

    # ---------------- RAW PARQUET ----------------
    if os.path.exists(RAW_DATA_FILE):
        old_raw = pd.read_parquet(RAW_DATA_FILE)
        raw_df = pd.concat([old_raw, raw_df], ignore_index=True)
        raw_df = raw_df.drop_duplicates(
            subset=["date", "ticker"],
            keep="last"
        )

    raw_df.to_parquet(RAW_DATA_FILE, index=False)
    print("Raw parquet updated")

    # ---------------- CLEAN PARQUET ----------------
    encoder = load_or_create_encoder(tickers)

    clean_df = raw_df.copy()
    clean_df = encode_tickers(clean_df, encoder)
    clean_df = add_features(clean_df)
    clean_df = drop_bad_index_columns(clean_df)

    FINAL_COLUMNS = [
        "date", "open", "high", "low", "close", "adj close", "volume",
        "ticker", "ticker_id",
        "daily_return", "volume_change",
        "ma20", "ma50", "close_ma20_ratio", "volatility",
        "rsi", "ema12", "ema26", "macd", "macd_signal"
    ]

    clean_df = clean_df[FINAL_COLUMNS]
    clean_df = clean_df.sort_values(["ticker", "date"])

    clean_df.to_parquet(CLEAN_DATA_FILE, index=False)
    print("Clean parquet updated till", END_DATE)


if __name__ == "__main__":
    run_pipeline()
