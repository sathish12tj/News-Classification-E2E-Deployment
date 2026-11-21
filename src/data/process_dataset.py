"""
Module: process_dataset.py
Lifecycle Stage 4: Data Preparation (Full Dataset Processing Pipeline)
Combines headlines and articles, cleans the text at scale, and saves processed data.
"""

import os
import pandas as pd
from src.data.load_data import load_data
from src.data.preprocess import clean_batch


def process_dataset(raw_folder: str = "data/raw", output_path: str = "data/processed/cleaned_news.csv") -> pd.DataFrame:
    """
    Executes the complete data preparation pipeline:
    1. Loads multi-file raw CSVs.
    2. Combines headline and full article text for richer semantic signal.
    3. Runs high-speed batch text cleaning and lemmatization.
    4. Saves the resulting DataFrame to data/processed/cleaned_news.csv.
    """
    print("=" * 60)
    print("Stage 4: Data Preparation Pipeline Started")
    print("=" * 60)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = load_data(raw_folder)
    print(f"Raw records loaded: {len(df)}")

    # Combine headline + article text
    headline = df["news_headline"].fillna("").astype(str)
    article = df["news_article"].fillna("").astype(str)
    combined = headline + " " + article

    print("Running batch text cleaning and spaCy lemmatization...")
    df["clean_text"] = clean_batch(combined)

    # Filter out records where cleaned text is empty
    initial_count = len(df)
    df = df[df["clean_text"].str.strip().str.len() > 0].copy()
    print(f"Retained {len(df)} non-empty cleaned records (dropped {initial_count - len(df)}).")

    df.to_csv(output_path, index=False)
    print(f"Processed dataset saved successfully to '{output_path}'.")
    print("=" * 60)
    return df


if __name__ == "__main__":
    process_dataset()
