import pandas as pd
import joblib

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

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


def evaluate_thresholds(model, X_test, y_test):
    y_proba = model.predict_proba(X_test)[:, 1]

    thresholds = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

    results = []

    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)

        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

        results.append(
            {
                "threshold": threshold,
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, zero_division=0),
                "recall": recall_score(y_test, y_pred, zero_division=0),
                "f1_score": f1_score(y_test, y_pred, zero_division=0),
                "true_negatives": tn,
                "false_positives": fp,
                "false_negatives": fn,
                "true_positives": tp,
            }
        )

    return pd.DataFrame(results)


def main():
    X_test, y_test = load_test_data()
    model = load_model()

    results_df = evaluate_thresholds(model, X_test, y_test)

    print("\nThreshold analysis on test set:")
    print(results_df)

    best_f1_row = results_df.loc[results_df["f1_score"].idxmax()]
    best_recall_row = results_df.loc[results_df["recall"].idxmax()]
    best_precision_row = results_df.loc[results_df["precision"].idxmax()]

    print("\nBest threshold by F1-score:")
    print(best_f1_row)

    print("\nBest threshold by recall:")
    print(best_recall_row)

    print("\nBest threshold by precision:")
    print(best_precision_row)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = METRICS_DIR / "final_threshold_analysis.csv"
    results_df.to_csv(output_path, index=False)

    print(f"\nFinal threshold analysis saved to: {output_path}")


if __name__ == "__main__":
    main()