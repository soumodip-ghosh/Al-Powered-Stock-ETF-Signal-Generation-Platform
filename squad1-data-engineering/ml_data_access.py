import pandas as pd
import os
import sys

# Add src to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fetch_data import fetch_data
from clean_data import clean_data
from feature_engineering import generate_features

def get_processed_dataframe(ticker, start_date, end_date):
  
    print(f"\n{'='*60}")
    print(f"Processing {ticker} ({start_date} to {end_date})")
    print(f"{'='*60}")
    
    # Step 1: Fetch raw data using existing function
    fetch_data(ticker=ticker, start_date=start_date, end_date=end_date)
    
    # Step 2: Clean data using existing function
    clean_data(ticker=ticker)
    
    # Step 3: Generate features using existing function
    generate_features(ticker=ticker)
    
    # Step 4: Read the processed data
    final_path = f"data/processed/{ticker}_final.csv"
    if not os.path.exists(final_path):
        raise FileNotFoundError(f"Processed file not found: {final_path}")
    
    df = pd.read_csv(final_path, index_col='date', parse_dates=True)
    
    # Step 5: Standardize column names for ML team
    rename_map = {
        'daily_return': 'Return',
        'ma_20': 'SMA_20',
        'ma_50': 'SMA_50',
        'rsi_14': 'RSI_14',
        'macd': 'MACD',
        'volatility': 'Volatility'
    }
    df.rename(columns=rename_map, inplace=True)
    
    # Step 6: Add Ticker column
    df['Ticker'] = ticker
    
    print(f"✅ Completed processing for {ticker}. Shape: {df.shape}")
    return df


def get_all_tickers_dataframe(tickers, start_date, end_date):
    
    print(f"\nProcessing {len(tickers)} tickers: {tickers}")
    all_data = []
    
    for ticker in tickers:
        try:
            df = get_processed_dataframe(ticker, start_date, end_date)
            all_data.append(df)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue
    
    if all_data:
        print("\nConsolidating all ticker data...")
        master_df = pd.concat(all_data, ignore_index=True)
        print(f"Consolidated DataFrame shape: {master_df.shape}")
        print(f"Tickers included: {master_df['Ticker'].unique().tolist()}")
        return master_df
    else:
        print("No data to consolidate.")
        return pd.DataFrame()


