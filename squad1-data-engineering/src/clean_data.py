import pandas as pd
import os

def clean_data(ticker="AAPL"):
    """
    Loads raw data, cleans it, and saves it to the processed folder.
    
    Parameters:
        ticker (str): The stock or ETF symbol (default: "AAPL").
    """
    
    # define paths
    raw_path = f"data/raw/{ticker}_raw.csv"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    processed_path = f"{processed_dir}/{ticker}_cleaned.csv"
    
    print(f"Cleaning data for {ticker}...")
    
    # load raw data
    # explicitly parse the 'Date' column if it exists, otherwise we'll handle it below
    try:
        df = pd.read_csv(raw_path)
    except FileNotFoundError:
        print(f"Error: File not found at {raw_path}")
        return

    # standardize column names to lowercase
    df.columns = [col.lower() for col in df.columns]
    
    # ensure date column is datetime
    # yfinance usually puts Date in the index or as a column named 'Date' (now 'date')
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    elif df.index.name == 'Date':
         df.index.name = 'date'
         df.index = pd.to_datetime(df.index)

    # drop missing values
    df.dropna(inplace=True)
    
    # save to csv
    df.to_csv(processed_path)
    print(f"Cleaned data saved to {processed_path}")

if __name__ == "__main__":
    clean_data()
