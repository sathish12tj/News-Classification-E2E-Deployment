"""
Module: vectorizer.py
Lifecycle Stage 4: Feature Extraction (Vectorization)
Fits TF-IDF and CountVectorizer feature pipelines on the cleaned news corpus.
"""

import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def build_and_save_vectorizer(
    data_path: str = "data/processed/cleaned_news.csv",
    vectorizer_path: str = "models/tfidf_vectorizer.pkl",
    max_features: int = 20000,
    ngram_range: tuple = (1, 2)
):
    """
    Fits a TF-IDF vectorizer with unigram and bigram features up to max_features,
    and serializes the fitted vectorizer to disk.
    """
    print("=" * 60)
    print("Stage 4: Feature Extraction (TF-IDF Vectorization)")
    print("=" * 60)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned dataset not found at '{data_path}'. Run data preparation first.")

    os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
    df = pd.read_csv(data_path)
    df["clean_text"] = df["clean_text"].fillna("")

    print(f"Fitting TfidfVectorizer (max_features={max_features}, ngram_range={ngram_range}) on {len(df)} documents...")
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        sublinear_tf=True,
        norm="l2"
    )

    X = vectorizer.fit_transform(df["clean_text"])
    print(f"Feature matrix shape: {X.shape} (articles x features)")
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)} terms")

    joblib.dump(vectorizer, vectorizer_path)
    print(f"TF-IDF Vectorizer successfully saved to '{vectorizer_path}'.")
    print("=" * 60)
    return vectorizer, X


def get_count_vectorizer(max_features: int = 20000, ngram_range: tuple = (1, 2)) -> CountVectorizer:
    """Alternative CountVectorizer (Bag-of-Words baseline) as outlined in the guide."""
    return CountVectorizer(max_features=max_features, ngram_range=ngram_range)


if __name__ == "__main__":
    build_and_save_vectorizer()
