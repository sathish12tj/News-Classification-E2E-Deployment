"""
Module: store.py
Lifecycle Stage 9: Category-Feed Routing & Persistence Store
Routes classified news articles to category-specific data stores (data/feeds/{category}.csv),
powering downstream search indexers, recommendation engines, and daily news feeds.
"""

import os
import csv
import pandas as pd
from datetime import datetime

FEED_DIR = "data/feeds"


def route_article(text: str, category: str, headline: str = "", confidence: float = 1.0, metadata: dict = None) -> str:
    """
    Appends a classified article to the appropriate category feed CSV file with a timestamp.
    Returns the file path where the article was filed.
    """
    os.makedirs(FEED_DIR, exist_ok=True)
    clean_cat = str(category).lower().strip()
    path = os.path.join(FEED_DIR, f"{clean_cat}.csv")
    new_file = not os.path.exists(path)

    # Clean text of newlines for CSV row safety
    safe_text = " ".join(str(text).split())
    safe_headline = " ".join(str(headline).split()) if headline else safe_text[:80] + "..."

    timestamp = datetime.now().isoformat()

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "category", "confidence", "headline", "text"])
        writer.writerow([timestamp, clean_cat, f"{confidence:.4f}", safe_headline, safe_text])

    return path


def get_feed(category: str, limit: int = 50) -> list:
    """Retrieves the most recent articles from a specified category feed."""
    clean_cat = str(category).lower().strip()
    path = os.path.join(FEED_DIR, f"{clean_cat}.csv")
    if not os.path.exists(path):
        return []

    try:
        df = pd.read_csv(path)
        records = df.tail(limit).to_dict(orient="records")
        records.reverse()  # Latest first
        return records
    except Exception as e:
        print(f"Error reading feed '{category}': {e}")
        return []


def get_all_feed_stats() -> dict:
    """Returns article counts and status across all category feeds."""
    os.makedirs(FEED_DIR, exist_ok=True)
    stats = {}
    total_articles = 0
    for filename in sorted(os.listdir(FEED_DIR)):
        if filename.endswith(".csv"):
            cat = filename.replace(".csv", "")
            filepath = os.path.join(FEED_DIR, filename)
            try:
                df = pd.read_csv(filepath)
                count = len(df)
                last_updated = df["timestamp"].iloc[-1] if not df.empty else None
            except Exception:
                count = 0
                last_updated = None
            stats[cat] = {
                "article_count": count,
                "last_updated": last_updated
            }
            total_articles += count
    return {
        "total_routed_articles": total_articles,
        "categories": stats
    }


if __name__ == "__main__":
    # Test routing
    test_headline = "Apple announces M4 chips with major AI acceleration"
    test_article = "Apple today introduced the latest generation of silicon designed for intensive AI workflows."
    saved_path = route_article(test_article, "technology", headline=test_headline, confidence=0.985)
    print(f"Test article routed to: {saved_path}")
    print("Feed summary:", get_all_feed_stats())
