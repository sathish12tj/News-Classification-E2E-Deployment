"""
Module: preprocess.py
Lifecycle Stage 4: Data Preparation (Text Cleaning & Normalization)
Tokenization, lower-casing, regex filtering, stop-word removal, and spaCy lemmatization.
"""

import re
import spacy

# Load spaCy small English pipeline
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """
    Cleans a single news article or headline string.
    1. Converts to lowercase.
    2. Removes URLs.
    3. Strips punctuation, digits, and special characters.
    4. Tokenizes, removes stop-words, and lemmatizes using spaCy.
    """
    if not text or not isinstance(text, str):
        return ""

    # Vectorized / fast string operations
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    doc = nlp(text)
    words = [token.lemma_ for token in doc if not token.is_stop and len(token.lemma_) > 1]
    return " ".join(words)


def clean_batch(texts, batch_size: int = 500) -> list:
    """
    Streams a collection of texts through spaCy's nlp.pipe in batches,
    disabling unnecessary pipeline components (parser, NER) for high-throughput batch preprocessing.
    """
    # Pre-clean strings with fast regex first
    cleaned_inputs = []
    for t in texts:
        s = str(t).lower()
        s = re.sub(r"http\S+|www\S+", "", s)
        s = re.sub(r"[^a-zA-Z\s]", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        cleaned_inputs.append(s)

    docs = nlp.pipe(cleaned_inputs, disable=["parser", "ner"], batch_size=batch_size)

    cleaned_texts = []
    for doc in docs:
        words = [t.lemma_ for t in doc if not t.is_stop and len(t.lemma_) > 1]
        cleaned_texts.append(" ".join(words))

    return cleaned_texts


if __name__ == "__main__":
    sample = "Global smartphone sales in Q3 fall 5.7% to 36.6 cr units: Gartner reports https://example.com"
    print("Original:", sample)
    print("Cleaned: ", clean_text(sample))
