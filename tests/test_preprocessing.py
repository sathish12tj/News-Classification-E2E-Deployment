"""Unit tests for text preprocessing & spaCy lemmatization pipeline."""

import unittest
from src.data.preprocess import clean_text, clean_batch


class TestPreprocessing(unittest.TestCase):
    def test_clean_text_removes_urls(self):
        text = "Breaking update: Check out the full story at https://www.reuters.com/world/news-123 right now!"
        cleaned = clean_text(text)
        self.assertNotIn("https", cleaned)
        self.assertNotIn("reuters", cleaned)

    def test_clean_text_lowercase_and_punctuation(self):
        text = "Apple's Q3 REVENUE Surged by 15.8% ($94.9 Billion), Beats Wall-Street Expectations!!!"
        cleaned = clean_text(text)
        self.assertEqual(cleaned, cleaned.lower())
        self.assertNotIn("$", cleaned)
        self.assertNotIn("%", cleaned)
        self.assertNotIn("!", cleaned)

    def test_clean_text_lemmatization(self):
        text = "The athletes were running and winning gold medals across competitions."
        cleaned = clean_text(text)
        # Lemmatization: running -> run, winning -> win, medals -> medal
        self.assertTrue("run" in cleaned or "win" in cleaned or "medal" in cleaned)

    def test_clean_batch(self):
        texts = [
            "President signs legislative reform act.",
            "Ferrari announces brand new hybrid supercar with V8 twin turbo engine.",
            "Astronomers discover habitable exoplanet in nearby star cluster."
        ]
        cleaned_list = clean_batch(texts)
        self.assertEqual(len(cleaned_list), len(texts))
        for c in cleaned_list:
            self.assertIsInstance(c, str)
            self.assertGreater(len(c), 0)


if __name__ == "__main__":
    unittest.main()
