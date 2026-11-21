"""
Module: app.py
Lifecycle Stage 9: Model Deployment (FastAPI Web Service & Live UI)
Exposes RESTful endpoints for real-time inference, batch prediction,
daily live feed ingestion, feed exploration, model performance metrics, and dashboard UI.
"""

import os
import json
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.models.predict import NewsClassifier
from src.routing.store import route_article, get_feed, get_all_feed_stats
from src.live.live_feed import run_daily_live_ingestion

app = FastAPI(
    title="News Classification & Real-Time Content Routing Engine",
    description="End-to-End NLP multi-class news categorization and live feed routing system powered by Linear SVM and TF-IDF.",
    version="1.0.0"
)

# Enable CORS for external frontends or integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model classifier instance
classifier = None


@app.on_event("startup")
def load_classifier_on_startup():
    global classifier
    try:
        classifier = NewsClassifier()
        print("NewsClassifier loaded and initialized successfully on startup.")
    except Exception as e:
        print(f"Warning: NewsClassifier could not be loaded at startup: {e}")


# --- Pydantic Schemas ---
class ArticleRequest(BaseModel):
    text: str = Field(..., description="Full text or headline of the news article", example="DeepMind's AlphaFold predicts 3D structure of human proteins with pinpoint accuracy.")
    headline: Optional[str] = Field(None, description="Optional headline", example="AlphaFold solves 50-year protein folding challenge")
    auto_route: bool = Field(True, description="Whether to automatically append this article to its category feed")


class BatchArticleRequest(BaseModel):
    articles: List[ArticleRequest]


class PredictionResponse(BaseModel):
    category: str
    confidence: float
    cleaned_text: str
    category_scores: dict
    routed_feed: Optional[str] = None
    timestamp: str


# --- API Endpoints ---

@app.get("/health", tags=["System"])
def health_check():
    """Health status and model readiness endpoint."""
    return {
        "status": "healthy",
        "service": "News Classification & Routing API",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": classifier is not None,
        "supported_categories": classifier.classes if classifier else []
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
def predict_news(request: ArticleRequest):
    """
    Classifies a news article into one of the news categories (Technology, Sports, Politics, etc.),
    computes confidence scores, and automatically routes the article to its category feed.
    """
    global classifier
    if classifier is None:
        classifier = NewsClassifier()

    combined_text = request.text
    if request.headline and request.headline not in request.text:
        combined_text = f"{request.headline}. {request.text}"

    result = classifier.predict(combined_text)
    category = result["category"]
    confidence = result["confidence"]

    routed_path = None
    if request.auto_route and category != "unknown":
        routed_path = route_article(
            text=request.text,
            category=category,
            headline=request.headline or request.text[:80],
            confidence=confidence
        )

    return {
        "category": category,
        "confidence": confidence,
        "cleaned_text": result["cleaned_text"],
        "category_scores": result["category_scores"],
        "routed_feed": routed_path,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/batch_predict", tags=["Inference"])
def batch_predict_news(request: BatchArticleRequest):
    """Batch prediction endpoint for classifying multiple articles in a single payload."""
    global classifier
    if classifier is None:
        classifier = NewsClassifier()

    results = []
    for art in request.articles:
        combined = art.text
        if art.headline and art.headline not in art.text:
            combined = f"{art.headline}. {art.text}"
        res = classifier.predict(combined)
        routed = None
        if art.auto_route and res["category"] != "unknown":
            routed = route_article(art.text, res["category"], headline=art.headline or art.text[:80], confidence=res["confidence"])
        results.append({
            "headline": art.headline,
            "category": res["category"],
            "confidence": res["confidence"],
            "routed_feed": routed
        })
    return {"total": len(results), "results": results}


@app.get("/categories", tags=["Feeds"])
def list_categories():
    """Returns the list of all supported news categories."""
    global classifier
    if classifier is None:
        classifier = NewsClassifier()
    return {"categories": classifier.classes}


@app.get("/feeds/summary", tags=["Feeds"])
def feeds_summary():
    """Returns article volume and recent updates across all category feeds."""
    return get_all_feed_stats()


@app.get("/feed/{category}", tags=["Feeds"])
def read_category_feed(category: str, limit: int = Query(30, ge=1, le=200)):
    """Retrieves the latest routed articles from a specific category feed."""
    articles = get_feed(category, limit=limit)
    return {
        "category": category,
        "count": len(articles),
        "articles": articles
    }


@app.post("/live/ingest", tags=["Live News"])
def trigger_live_ingestion(max_per_feed: int = Query(4, ge=1, le=10)):
    """
    Triggers the live daily news ingestion pipeline:
    Fetches real-time headlines from global feeds, classifies them with Linear SVM,
    and files them into category feeds.
    """
    global classifier
    if classifier is None:
        classifier = NewsClassifier()

    digest = run_daily_live_ingestion(max_per_feed=max_per_feed, classifier=classifier)
    return {
        "status": "success",
        "ingested_count": len(digest),
        "articles": digest
    }


@app.get("/metrics", tags=["Analytics"])
def get_model_metrics():
    """Retrieves model evaluation report and metrics JSON."""
    metrics_path = "models/evaluation_report.json"
    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="Evaluation metrics not generated yet. Run evaluation first.")
    with open(metrics_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/metrics/confusion_matrix_image", tags=["Analytics"])
def get_confusion_matrix_image():
    """Returns the generated confusion matrix heatmap image."""
    img_path = "models/confusion_matrix.png"
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="Confusion matrix image not found. Run evaluation first.")
    return FileResponse(img_path, media_type="image/png")


@app.get("/metrics/category_chart_image", tags=["Analytics"])
def get_category_chart_image():
    """Returns the generated per-category metrics bar chart image."""
    img_path = "models/category_metrics.png"
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="Category metrics image not found. Run evaluation first.")
    return FileResponse(img_path, media_type="image/png")


# --- Modern Interactive Dashboard UI ---
@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def serve_dashboard():
    """Serves the rich interactive Live News Intelligence Dashboard UI."""
    frontend_path = "frontend/index.html"
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>News Classification API is Live. Visit <a href='/docs'>/docs</a> for interactive API documentation.</h1>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
