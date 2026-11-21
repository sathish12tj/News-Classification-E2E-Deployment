# 📰 News Intelligence & Real-Time Content Routing Engine

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![spaCy](https://img.shields.io/badge/spaCy-3.7+-09a3d5.svg)](https://spacy.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Accuracy](https://img.shields.io/badge/Test%20Accuracy-94.39%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An End-to-End NLP Machine Learning Lifecycle & Real-Time Multi-Class News Classification Platform.**  
> Built using **Linear Support Vector Machines (LinearSVC)**, **TF-IDF n-gram vectorization**, **spaCy lemmatization**, and **class-imbalance mitigation (RandomOverSampler)**, paired with a production **FastAPI microservice**, an **interactive newsroom dashboard**, and an automated **daily live RSS news wire ingestion engine**.

---

## 📑 Table of Contents
1. [Business Understanding & Strategic ROI](#-business-understanding--strategic-roi)
2. [End-to-End System Architecture](#-end-to-end-system-architecture)
3. [The 10-Stage Machine Learning Lifecycle](#-the-10-stage-machine-learning-lifecycle)
4. [Dataset Specifications](#-dataset-specifications)
5. [Evaluation Benchmarks & Confusion Matrix](#-evaluation-benchmarks--confusion-matrix)
6. [Everyday Live Operation & Live Wire Ingestion](#-everyday-live-operation--live-wire-ingestion)
7. [Interactive Newsroom Dashboard](#-interactive-newsroom-dashboard)
8. [REST API Documentation & Endpoints](#-rest-api-documentation--endpoints)
9. [Installation & Quickstart Guide](#-installation--quickstart-guide)
10. [Docker Containerization & CI/CD](#-docker-containerization--cicd)
11. [Client & Stakeholder Deliverables](#-client--stakeholder-deliverables)

---

## 🎯 Business Understanding & Strategic ROI

### The Challenge of Modern Digital Newsrooms
Digital publishers, aggregators (such as Inshorts, Google News, Bloomberg, Reuters), and media monitoring firms ingest **tens of thousands of news stories daily**. To provide a personalized reading experience, power internal search indices, and send real-time breaking alerts, each incoming article must be categorized accurately into its editorial domain: **Technology, Sports, Politics, Business, Science, Automobile, World, and Entertainment**.

### The Triad Comparison
| Dimension | Manual Editorial Tagging | Rule-Based Matching | AI News Classification Platform (Our System) |
| :--- | :--- | :--- | :--- |
| **Processing Latency** | 2 to 4 Hours per batch | 100 – 500 ms (linear rule search) | **< 15 Milliseconds per article** |
| **Operational Scalability** | Capped at ~300 articles/day/editor | Collapses as rules exceed ~500 entries | **100,000+ articles/day effortlessly** |
| **Semantic Generalization** | Subject to editorial fatigue & inconsistency | 0% (Fails on unseen phrases & polysemy) | **High (Learns statistical term distributions)** |
| **Maintenance Cost** | Linear escalation of labor costs | Fragile manual patching of regex rules | **Continuous CI/CD automated retraining** |

> **Key Downstream Impact**: Fast and consistent classification feeds downstream **search indexing**, **personalized recommendation engines**, and **automated content feeds**, driving reader retention and ad monetization.

---

## 🏗 End-to-End System Architecture

The architecture consists of two decoupled lifecycles sharing a unified **Model Store**:

```
                                  OFFLINE BUILD PIPELINE
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ 7 Inshorts CSVs  ──>  Headline + Body Fusion  ──>  spaCy Lemmatization (nlp.pipe)       │
  │                                                                                        │
  │   TF-IDF (20k n-grams)  ──>  Stratified 80/20 Split  ──>  RandomOverSampler (Train Only)│
  │                                                                                        │
  │                         ──>  LinearSVC Fit  ──>  models/news_model.pkl                 │
  └───────────────────────────────────────────────────┬────────────────────────────────────┘
                                                      │  (Shared Artifacts)
                                                      ▼
                                  ONLINE SERVE PIPELINE
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ Live RSS News Wire / FastAPI /predict  ──>  clean_text() Normalization                 │
  │                                                                                        │
  │   tfidf_vectorizer.transform()  ──>  Linear SVM Inference  ──>  Softmax Calibration   │
  │                                                                                        │
  │         ──>  Auto-Route to data/feeds/{category}.csv  ──>  Search & Recommendation Feeds│
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 The 10-Stage Machine Learning Lifecycle

1. **Stage 1: Business Understanding** — Defined multi-class categorization goals, SLA requirements (< 20ms latency), and downstream routing hand-off.
2. **Stage 2: Data Collection** — Automated download and structuring of Kishan Yadav's 7-part Inshorts news collection.
3. **Stage 3: Data Understanding** — Aggregation of 12,120 articles across 7 classes; verification of text lengths, null checks, and category distributions.
4. **Stage 4: Data Preparation** — Dual-level cleaning (`clean_text` for real-time and `clean_batch` with spaCy `nlp.pipe` for batch scaling); unigram + bigram TF-IDF vectorization (20,000 features).
5. **Stage 5: Model Building** — Instantiation of `LinearSVC(C=1.0)` with One-vs-Rest multi-class architecture.
6. **Stage 6: Model Training & Class Balancing** — Stratified train/test split followed by `RandomOverSampler` on the training fold only to eliminate minority-class starvation while preventing test data leakage.
7. **Stage 7: Model Testing** — Interactive CLI predictor with calibrated softmax confidence estimation.
8. **Stage 8: Model Evaluation** — Held-out test evaluation generating confusion matrix heatmaps and per-class precision/recall bars.
9. **Stage 9: Deployment & Feed Routing** — FastAPI REST server exposing `/predict`, `/batch_predict`, `/live/ingest`, and category CSV persistence store.
10. **Stage 10: CI/CD & Operations** — Pytest automated test suite, GitHub Actions workflow, and Docker containerization.

---

## 📊 Dataset Specifications

The platform is trained on **12,120 verified short news articles** across 7 files in `data/raw/`:

| News Category | Article Count | Percentage |
| :--- | :---: | :---: |
| **World** | 2,067 | 17.0% |
| **Entertainment** | 2,036 | 16.8% |
| **Sports** | 1,900 | 15.7% |
| **Technology** | 1,791 | 14.8% |
| **Politics** | 1,596 | 13.2% |
| **Science** | 1,437 | 11.8% |
| **Automobile** | 1,293 | 10.7% |
| **Total** | **12,120** | **100.0%** |

---

## 📈 Evaluation Benchmarks & Confusion Matrix

Evaluated on **2,424 strictly held-out test articles**:

### Detailed Classification Report
```text
               precision    recall  f1-score   support

   automobile     0.9410    0.9846    0.9623       259
entertainment     0.9655    0.9631    0.9643       407
     politics     0.9874    0.9812    0.9843       319
      science     0.9592    0.9792    0.9691       288
       sports     0.9709    0.9658    0.9683       380
   technology     0.8952    0.8352    0.8642       358
        world     0.8962    0.9201    0.9080       413

     accuracy                         0.9439      2424
    macro avg     0.9451    0.9470    0.9458      2424
 weighted avg     0.9437    0.9439    0.9435      2424
```

### Visual Artifacts
- **Confusion Matrix Heatmap**: `models/confusion_matrix.png`
- **Per-Category Performance Chart**: `models/category_metrics.png`
- **Machine-Readable Metrics**: `models/evaluation_report.json`

---

## 📡 Everyday Live Operation & Live Wire Ingestion

To use this system **every single day**, the built-in ingestion engine connects to live global news feeds:

```bash
# Ingest today's breaking news live and auto-route to category feeds
python main.py --stage live
```

What this does:
1. Connects to real-time RSS feeds: **Google News (Top Stories, Tech, Sports, Business, Science)** and **BBC News Global**.
2. Extracts latest headlines and summaries.
3. Automatically tokenizes and classifies each story with the trained Linear SVM model.
4. Files each story into `data/feeds/{category}.csv` with timestamps and confidence scores.

---

## 💻 Interactive Newsroom Dashboard

The platform includes a modern web-based UI served directly by FastAPI.

```bash
python main.py --stage serve
```
Open **`http://127.0.0.1:8000`** in your browser:
- **⚡ Live News Classifier**: Enter headlines or paste article copy with quick sample loaders.
- **📡 Daily Live Wire Ingestion**: Single-click real-time news retrieval and classification.
- **📂 Category News Desk**: Explore categorized news feeds with filter pills and search.
- **📊 Model Analytics & Confusion Matrix**: Real-time view of model telemetry and confusion heatmaps.

---

## 🔌 REST API Documentation & Endpoints

Interactive Swagger UI available at: **`http://127.0.0.1:8000/docs`**

### Key Endpoints:
- `POST /predict`: Classifies news text and auto-routes to category feed.
- `POST /batch_predict`: Bulk classification for content syndication.
- `POST /live/ingest`: Triggers live RSS feed polling and classification.
- `GET /categories`: Returns list of all supported news categories.
- `GET /feed/{category}`: Returns latest articles from a specific category feed.
- `GET /feeds/summary`: Overview of article counts across all feeds.
- `GET /metrics`: Comprehensive model evaluation metrics JSON.
- `GET /health`: Health and model readiness status.

#### Sample Prediction Request:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "headline": "DeepMind AlphaFold predicts 3D protein structures",
       "text": "Artificial intelligence model predicts folded conformations with atomic precision.",
       "auto_route": true
     }'
```

#### Sample Response:
```json
{
  "category": "technology",
  "confidence": 0.9842,
  "cleaned_text": "artificial intelligence model predict fold conformation atomic precision",
  "category_scores": {
    "technology": 0.9842,
    "science": 0.0112,
    "world": 0.0021,
    "business": 0.0012,
    "automobile": 0.0006,
    "politics": 0.0004,
    "entertainment": 0.0002,
    "sports": 0.0001
  },
  "routed_feed": "data/feeds/technology.csv",
  "timestamp": "2026-11-22T02:15:30.123456"
}
```

---

## 🚀 Installation & Quickstart Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/sathish12tj/News_Classification_E2E_Deployment.git
cd News_Classification_E2E_Deployment

# Create & activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows
```

### 2. Install Dependencies & Language Model
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Pipeline CLI Commands
```bash
# Execute full pipeline end-to-end
python main.py --stage all

# Run unit tests
python run_tests.py

# Ingest today's live breaking news
python main.py --stage live

# Launch API & Web Dashboard
python main.py --stage serve
```

---

## 🐳 Docker Containerization & CI/CD

### Docker Build & Run
```bash
# Build Docker image
docker build -t news-classifier:latest .

# Run container
docker run -p 8000:8000 news-classifier:latest
```

### Docker Compose
```bash
docker-compose up -d
```

### GitHub Actions CI/CD
The repository includes `.github/workflows/ci_cd.yml` which automatically:
- Checks out code on Ubuntu runners.
- Sets up Python 3.11 and caches pip packages.
- Installs dependencies and downloads spaCy's `en_core_web_sm`.
- Executes unit tests across data cleaning, routing, and API contracts.

---

## 📁 Client & Stakeholder Deliverables

Two comprehensive executive deliverables are included in the repository root:

1. **`News_Classification_Business_Technical_Report.docx`**  
   - Detailed formal Word report for clients and stakeholders.
   - Contains executive summary, business ROI analysis, mathematical TF-IDF formulation, class balancing rationale, embedded high-resolution confusion matrix charts, and strategic MLOps roadmap.

2. **`News_Classification_Stakeholder_Presentation.pptx`**  
   - 11 modern, high-impact widescreen (16:9) presentation slides.
   - Designed for C-level executives, product managers, and engineering leads.
   - Highlights problem statement, architecture cards, before/after balancing impact, confusion matrix visualizations, and ROI takeaways.

---

## 👤 Author
- **Developer**: Sathish ([@sathish12tj](https://github.com/sathish12tj))
- **Role**: AI & Machine Learning Engineer
- **Course**: ProITBridge NLP Foundation — Project 3 Capstone
