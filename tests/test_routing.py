"""Unit tests for category-feed store and routing logic."""

import os
import unittest
import pandas as pd
from src.routing.store import route_article, get_feed, get_all_feed_stats


class TestRoutingStore(unittest.TestCase):
    def test_route_article(self):
        test_headline = "Test Headline: Quantum Supremacy Reached"
        test_text = "Scientists have demonstrated quantum computational advantage over classical algorithms."
        category = "technology"

        path = route_article(test_text, category, headline=test_headline, confidence=0.99)
        self.assertTrue(os.path.exists(path))

        df = pd.read_csv(path)
        self.assertGreater(len(df), 0)
        self.assertIn("headline", df.columns)
        self.assertIn("text", df.columns)
        self.assertIn("confidence", df.columns)

    def test_get_feed(self):
        feed = get_feed("technology", limit=5)
        self.assertIsInstance(feed, list)
        if feed:
            self.assertIn("headline", feed[0])
            self.assertIn("text", feed[0])

    def test_get_all_feed_stats(self):
        stats = get_all_feed_stats()
        self.assertIn("total_routed_articles", stats)
        self.assertIn("categories", stats)


if __name__ == "__main__":
    unittest.main()
