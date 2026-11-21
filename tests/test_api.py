"""Unit tests for FastAPI endpoints."""

import unittest
from src.api.app import app, health_check, feeds_summary, predict_news, ArticleRequest


class TestAPIEndpoints(unittest.TestCase):
    def test_health_endpoint(self):
        data = health_check()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("model_loaded", data)

    def test_predict_endpoint_contract(self):
        req = ArticleRequest(
            text="The football team secured an incredible victory in the Champions League final.",
            headline="Champions League Final Triumph",
            auto_route=True
        )
        data = predict_news(req)
        self.assertEqual(data["category"], "sports")
        self.assertGreater(data["confidence"], 0.5)
        self.assertIn("category_scores", data)

    def test_feeds_summary_endpoint(self):
        data = feeds_summary()
        self.assertIn("categories", data)


if __name__ == "__main__":
    unittest.main()
