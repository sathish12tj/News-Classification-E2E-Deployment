"""
Module: load_data.py
Lifecycle Stage 3: Data Understanding
Loads and concatenates multi-file Inshorts news data.
"""

import glob
import os
import pandas as pd


def load_data(folder: str = "data/raw") -> pd.DataFrame:
    """
    Loads all inshort_news_data-*.csv files from the given folder
    and concatenates them into a unified pandas DataFrame.
    """
    pattern = os.path.join(folder, "inshort_news_data-*.csv")
    files = sorted(glob.glob(pattern))

    if not files:
        raise FileNotFoundError(f"No inshort_news_data-*.csv files found in '{folder}'.")

    print(f"Loading {len(files)} dataset files from '{folder}'...")
    frames = []
    for f in files:
        df = pd.read_csv(f)
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        frames.append(df)

    combined_df = pd.concat(frames, ignore_index=True)
    # Drop empty or corrupted rows
    combined_df = combined_df.dropna(subset=["news_headline", "news_category"])
    print(f"Successfully loaded {len(combined_df)} records across {len(files)} files.")
    return combined_df


if __name__ == "__main__":
    df = load_data("data/raw")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nCategory Distribution:")
    print(df["news_category"].value_counts())
