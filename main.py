"""
Main Pipeline Orchestrator
News Classification & Real-Time Content Routing Engine

Usage:
    python main.py --stage all            # Run full end-to-end pipeline (preprocess -> vectorize -> train -> evaluate)
    python main.py --stage preprocess     # Run text cleaning & spaCy lemmatization
    python main.py --stage vectorize      # Extract TF-IDF features
    python main.py --stage train          # Train Linear SVM with RandomOverSampler
    python main.py --stage evaluate       # Evaluate on test set & generate confusion matrix plots
    python main.py --stage test           # Run interactive CLI prediction tester
    python main.py --stage live           # Ingest, classify, and route today's real live news wire
    python main.py --stage serve          # Launch FastAPI service & Interactive Web Dashboard
"""

import sys
import argparse
import uvicorn

from src.data.process_dataset import process_dataset
from src.features.vectorizer import build_and_save_vectorizer
from src.models.train import train_model
from src.models.evaluate import evaluate_model
from src.models.predict import interactive_cli
from src.live.live_feed import run_daily_live_ingestion


def run_full_pipeline():
    print("\n" + "=" * 70)
    print("STARTING FULL END-TO-END NEWS CLASSIFICATION & ROUTING PIPELINE")
    print("=" * 70 + "\n")

    # Step 1: Preprocess dataset
    print("[1/4] Processing raw Inshorts CSV dataset...")
    process_dataset()

    # Step 2: Extract TF-IDF features
    print("\n[2/4] Fitting and serializing TF-IDF vectorizer...")
    build_and_save_vectorizer()

    # Step 3: Train model with class balancing
    print("\n[3/4] Training Linear SVM classifier with RandomOverSampling...")
    train_model(balance=True)

    # Step 4: Evaluate model and produce charts
    print("\n[4/4] Evaluating classifier on held-out test data & exporting plots...")
    evaluate_model()

    print("\n" + "=" * 70)
    print("FULL PIPELINE EXECUTED SUCCESSFULLY!")
    print("Model, Vectorizer, Metrics & Visualizations are ready.")
    print("Launch UI with: python main.py --stage serve")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="News Classification E2E Pipeline Orchestrator")
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=["all", "preprocess", "vectorize", "train", "evaluate", "test", "live", "serve"],
        help="Pipeline stage to execute"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for FastAPI web server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host for FastAPI web server")

    args = parser.parse_args()

    if args.stage == "all":
        run_full_pipeline()
    elif args.stage == "preprocess":
        process_dataset()
    elif args.stage == "vectorize":
        build_and_save_vectorizer()
    elif args.stage == "train":
        train_model()
    elif args.stage == "evaluate":
        evaluate_model()
    elif args.stage == "test":
        interactive_cli()
    elif args.stage == "live":
        run_daily_live_ingestion()
    elif args.stage == "serve":
        print(f"Starting News Intelligence Web Service on http://{args.host}:{args.port}")
        uvicorn.run("src.api.app:app", host=args.host, port=args.port, reload=True)


if __name__ == "__main__":
    main()
