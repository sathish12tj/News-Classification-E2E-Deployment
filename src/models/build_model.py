"""
Module: build_model.py
Lifecycle Stage 5: Model Building
Defines the classification algorithm architecture.
Linear Support Vector Classifier (LinearSVC) for high-dimensional sparse text representations.
"""

from sklearn.svm import LinearSVC


def build_model(C: float = 1.0, class_weight: str = None, random_state: int = 42) -> LinearSVC:
    """
    Builds and returns an untrained Linear Support Vector Classifier (LinearSVC).
    
    Why Linear SVM for NLP Text Classification:
    - Text represented via TF-IDF spans tens of thousands of dimensions (sparse feature space).
    - Linear SVM finds the maximum-margin hyperplane separating classes, maximizing geometric margin.
    - Highly resistant to overfitting in high dimensions compared to non-linear kernels.
    - Trains orders of magnitude faster than kernel SVMs on large corpora.
    - Multi-class classification handled via One-vs-Rest (OvR) formulation.
    """
    return LinearSVC(
        C=C,
        class_weight=class_weight,
        random_state=random_state,
        max_iter=3000,
        dual="auto"
    )


if __name__ == "__main__":
    clf = build_model()
    print("Instantiated Model Architecture:")
    print(clf)
