# auctions/scripts/extract_auction_minimal.py

import pandas as pd
import os

def extract_basic_info(file_path):
    ''' Extract title, price, and image link from the raw dataset '''
    df = pd.read_table(file_path)

    # Drop unnecessary unnamed column if it exists
    df = df.drop(columns='Unnamed: 0', errors='ignore')

    # Filter out rows with missing required fields
    df = df[df['name'].notnull() & df['price'].notnull() & df['source'].notnull()]

    # Keep only needed columns and rename for clarity
    df = df[['name', 'price', 'source']].copy()
    df.columns = ['Title', 'Price', 'LinkToImage']

    return df

if __name__ == "__main__":
    input_path = os.path.join('auctions', 'data', 'data.txt')
    output_path = os.path.join('auctions', 'data', 'artwork_minimal.csv')

    df_minimal = extract_basic_info(input_path)
    df_minimal.to_csv(output_path, index=False)

    print(f"✅ Saved minimal data to {output_path}")
