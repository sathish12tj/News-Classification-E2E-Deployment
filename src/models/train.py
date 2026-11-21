"""
Module: train.py
Lifecycle Stage 6: Model Training
Splits data into train and test sets, mitigates class imbalance via RandomOverSampler
on the training set only (preventing test leakage), fits LinearSVC, and saves model artifacts.
"""

import os
import json
import joblib
import pandas as pd
from collections import Counter
from datetime import datetime

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from src.models.build_model import build_model


def train_model(
    data_path: str = "data/processed/cleaned_news.csv",
    vectorizer_path: str = "models/tfidf_vectorizer.pkl",
    model_output_path: str = "models/news_model.pkl",
    balance: bool = True,
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Executes the model training lifecycle:
    1. Loads cleaned corpus and previously fitted TF-IDF vectorizer (transform only).
    2. Performs stratified train/test split.
    3. Balances the training fold using RandomOverSampler (if balance=True).
    4. Trains the LinearSVC model.
    5. Serializes model, test dataset cache, and training metadata.
    """
    print("=" * 60)
    print("Stage 6: Model Training Pipeline Started")
    print("=" * 60)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned dataset '{data_path}' not found.")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer '{vectorizer_path}' not found.")

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    df = pd.read_csv(data_path)
    df["clean_text"] = df["clean_text"].fillna("")

    print(f"Loading vectorizer from '{vectorizer_path}'...")
    vectorizer = joblib.load(vectorizer_path)

    print("Vectorizing text features...")
    X = vectorizer.transform(df["clean_text"])
    y = df["news_category"]

    print(f"Total dataset: {X.shape[0]} articles, {X.shape[1]} features.")

    # 1. Split FIRST - strictly keeping test set untouched
    print(f"Executing stratified train/test split (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    before_counts = Counter(y_train)
    print("\nTraining set distribution before balancing:")
    for cat, cnt in sorted(before_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat:15s}: {cnt}")

    # 2. Balance TRAINING split only
    if balance:
        print("\nApplying RandomOverSampler to training fold...")
        ros = RandomOverSampler(random_state=random_state)
        X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
        after_counts = Counter(y_train_resampled)
        print("Training set distribution after balancing:")
        for cat, cnt in sorted(after_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {cat:15s}: {cnt}")
        X_train, y_train = X_train_resampled, y_train_resampled
    else:
        print("Skipping resampling (balance=False).")
        after_counts = before_counts

    # 3. Fit Linear SVM
    print("\nTraining Linear Support Vector Machine...")
    model = build_model(C=1.0, random_state=random_state)
    model.fit(X_train, y_train)

    # 4. Save model artifact
    joblib.dump(model, model_output_path)
    print(f"Trained model saved to '{model_output_path}'.")

    # 5. Cache test data for evaluation & reproducibility
    test_cache_path = "models/test_data.pkl"
    joblib.dump((X_test, y_test), test_cache_path)
    print(f"Held-out test split cached to '{test_cache_path}'.")

    # 6. Save metadata
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "total_articles": int(len(df)),
        "categories": sorted(list(y.unique())),
        "train_samples_original": int(X_train.shape[0]) if not balance else int(sum(before_counts.values())),
        "train_samples_resampled": int(X_train.shape[0]),
        "test_samples": int(X_test.shape[0]),
        "feature_count": int(X.shape[1]),
        "balanced": balance,
        "classes_distribution_before": dict(before_counts),
        "classes_distribution_after": dict(after_counts)
    }
    with open("models/training_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 60)
    print("Training Completed Successfully!")
    print("=" * 60)
    return model, X_test, y_test


if __name__ == "__main__":
    train_model()
