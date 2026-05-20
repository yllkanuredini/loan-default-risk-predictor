import json
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

from src.config import (
    PROCESSED_DATA_DIR,
    TARGET_COLUMN,
    BEST_MODEL_PATH,
    METRICS_DIR,
)


def load_test_data():
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")

    X_test = test_df.drop(columns=[TARGET_COLUMN])
    y_test = test_df[TARGET_COLUMN]

    return X_test, y_test


def load_model():
    if not BEST_MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {BEST_MODEL_PATH}")

    return joblib.load(BEST_MODEL_PATH)


def evaluate_saved_model():
    X_test, y_test = load_test_data()
    model = load_model()

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    cm = confusion_matrix(y_test, y_pred)

    print("\nFinal Test Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    metrics_path = METRICS_DIR / "final_test_metrics.json"
    confusion_matrix_path = METRICS_DIR / "confusion_matrix.csv"
    report_path = METRICS_DIR / "classification_report.txt"

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

    pd.DataFrame(
        cm,
        index=["Actual No Default", "Actual Default"],
        columns=["Predicted No Default", "Predicted Default"]
    ).to_csv(confusion_matrix_path)

    with open(report_path, "w") as f:
        f.write(classification_report(y_test, y_pred, zero_division=0))

    print(f"\nFinal test metrics saved to: {metrics_path}")
    print(f"Confusion matrix saved to: {confusion_matrix_path}")
    print(f"Classification report saved to: {report_path}")


if __name__ == "__main__":
    evaluate_saved_model()