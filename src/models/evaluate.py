"""
Module: evaluate.py
Lifecycle Stage 8: Model Evaluation
Evaluates the trained Linear SVM model on held-out test data.
Generates classification reports, confusion matrix tables, metrics JSON,
and high-resolution visualization charts for stakeholder presentation.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/script rendering
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support
)


def evaluate_model(
    model_path: str = "models/news_model.pkl",
    vectorizer_path: str = "models/tfidf_vectorizer.pkl",
    test_data_path: str = "models/test_data.pkl",
    output_dir: str = "models"
):
    """
    Evaluates model performance on the held-out test set:
    - Calculates overall accuracy, macro avg, weighted avg, and per-class precision/recall/F1.
    - Generates and prints the Confusion Matrix table.
    - Exports styled visualizations:
        - models/confusion_matrix.png
        - models/category_metrics.png
    - Saves models/evaluation_report.json.
    """
    print("=" * 60)
    print("Stage 8: Model Evaluation on Held-Out Test Set")
    print("=" * 60)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found.")
    if not os.path.exists(test_data_path):
        raise FileNotFoundError(f"Test split '{test_data_path}' not found.")

    os.makedirs(output_dir, exist_ok=True)
    model = joblib.load(model_path)
    X_test, y_test = joblib.load(test_data_path)

    print(f"Evaluating {X_test.shape[0]} test samples across {len(model.classes_)} classes...")
    predictions = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))
    labels = sorted(list(model.classes_))

    # Text report
    report_dict = classification_report(y_test, predictions, target_names=labels, output_dict=True)
    report_text = classification_report(y_test, predictions, target_names=labels, digits=4)
    print("\n--- Detailed Classification Report ---")
    print(report_text)

    # Confusion matrix
    cm = confusion_matrix(y_test, predictions, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print("\n--- Confusion Matrix (Rows = Actual, Columns = Predicted) ---")
    print(cm_df)

    # 1. Generate Confusion Matrix Plot
    plt.figure(figsize=(9, 7))
    sns.set_theme(style="white")
    ax = sns.heatmap(
        cm_df,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=True,
        linewidths=1.0,
        linecolor="#e0e0e0",
        square=True
    )
    plt.title(f"Linear SVM News Classification Confusion Matrix\nOverall Accuracy: {accuracy * 100:.2f}%", fontsize=14, fontweight="bold", pad=15)
    plt.ylabel("Actual News Category", fontsize=12, fontweight="bold")
    plt.xlabel("Predicted News Category", fontsize=12, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    cm_plot_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=300)
    plt.close()
    print(f"Confusion matrix plot saved to '{cm_plot_path}'.")

    # 2. Generate Per-Class Metrics Bar Chart
    precision, recall, f1, support = precision_recall_fscore_support(y_test, predictions, labels=labels)
    metrics_df = pd.DataFrame({
        "Category": labels,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "Support": support
    })

    plt.figure(figsize=(10, 6))
    x = np.arange(len(labels))
    width = 0.26
    plt.bar(x - width, metrics_df["Precision"], width, label="Precision", color="#1976D2")
    plt.bar(x, metrics_df["Recall"], width, label="Recall", color="#388E3C")
    plt.bar(x + width, metrics_df["F1-Score"], width, label="F1-Score", color="#F57C00")

    plt.xlabel("News Category", fontsize=12, fontweight="bold")
    plt.ylabel("Score (0.0 to 1.0)", fontsize=12, fontweight="bold")
    plt.title("Per-Category Evaluation Metrics (Linear SVM + TF-IDF)", fontsize=14, fontweight="bold", pad=15)
    plt.xticks(x, labels, rotation=45, ha="right", fontsize=10)
    plt.ylim(0, 1.1)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    bar_plot_path = os.path.join(output_dir, "category_metrics.png")
    plt.savefig(bar_plot_path, dpi=300)
    plt.close()
    print(f"Per-category metrics chart saved to '{bar_plot_path}'.")

    # 3. Export JSON report
    summary = {
        "overall_accuracy": round(accuracy, 4),
        "total_test_samples": int(X_test.shape[0]),
        "macro_avg": report_dict.get("macro avg", {}),
        "weighted_avg": report_dict.get("weighted avg", {}),
        "per_class_metrics": {
            cat: {
                "precision": round(report_dict[cat]["precision"], 4),
                "recall": round(report_dict[cat]["recall"], 4),
                "f1_score": round(report_dict[cat]["f1-score"], 4),
                "support": int(report_dict[cat]["support"])
            }
            for cat in labels if cat in report_dict
        },
        "confusion_matrix": cm.tolist(),
        "labels": labels
    }
    report_json_path = os.path.join(output_dir, "evaluation_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Evaluation report JSON saved to '{report_json_path}'.")
    print("=" * 60)
    return summary


if __name__ == "__main__":
    evaluate_model()
