import time
import joblib
import json
from datetime import datetime

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from src.config import (
    PROCESSED_DATA_DIR,
    TARGET_COLUMN,
    RANDOM_STATE,
    METRICS_DIR,
    MODELS_DIR,
    BEST_MODEL_PATH,
    MODEL_METADATA_PATH,
)

from src.features import get_feature_columns, build_preprocessor


def load_data():
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "validation.csv")

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN])
    y_val = val_df[TARGET_COLUMN]

    return X_train, X_val, y_train, y_val, train_df


def evaluate_model(model_name, model, X_val, y_val, training_time, params):
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    return {
        "model": model_name,
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred, zero_division=0),
        "recall": recall_score(y_val, y_pred, zero_division=0),
        "f1_score": f1_score(y_val, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_val, y_proba),
        "training_time_seconds": training_time,
        "params": str(params),
    }


def main():
    X_train, X_val, y_train, y_val, train_df = load_data()

    numerical_columns, categorical_columns = get_feature_columns(train_df)
    preprocessor = build_preprocessor(numerical_columns, categorical_columns)

    param_sets = [
        {
            "n_estimators": 150,
            "max_depth": 10,
            "min_samples_split": 20,
            "min_samples_leaf": 10,
            "class_weight": "balanced_subsample",
        },
        {
            "n_estimators": 200,
            "max_depth": 12,
            "min_samples_split": 20,
            "min_samples_leaf": 10,
            "class_weight": "balanced_subsample",
        },
        {
            "n_estimators": 200,
            "max_depth": 14,
            "min_samples_split": 20,
            "min_samples_leaf": 8,
            "class_weight": "balanced_subsample",
        },
        {
            "n_estimators": 250,
            "max_depth": 16,
            "min_samples_split": 15,
            "min_samples_leaf": 6,
            "class_weight": "balanced_subsample",
        },
        {
            "n_estimators": 300,
            "max_depth": 18,
            "min_samples_split": 10,
            "min_samples_leaf": 5,
            "class_weight": "balanced_subsample",
        },
    ]

    all_results = []
    best_pipeline = None
    best_result = None

    for i, params in enumerate(param_sets, start=1):
        model_name = f"Random Forest Tuned {i}"

        print(f"\nTraining {model_name}...")
        print(params)

        classifier = RandomForestClassifier(
            **params,
            random_state=RANDOM_STATE,
            n_jobs=-1
        )

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", classifier),
            ]
        )

        start_time = time.time()
        pipeline.fit(X_train, y_train)
        training_time = time.time() - start_time

        result = evaluate_model(
            model_name,
            pipeline,
            X_val,
            y_val,
            training_time,
            params
        )

        all_results.append(result)

        print(f"{model_name} results:")
        for metric, value in result.items():
            if metric not in ["model", "params"]:
                print(f"{metric}: {value:.4f}")

        if best_result is None or result["f1_score"] > best_result["f1_score"]:
            best_result = result
            best_pipeline = pipeline

    results_df = pd.DataFrame(all_results)

    print("\nRandom Forest tuning results:")
    print(results_df)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = METRICS_DIR / "random_forest_tuning_results.csv"
    results_df.to_csv(output_path, index=False)

    print(f"\nTuning results saved to: {output_path}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_pipeline, BEST_MODEL_PATH)

    metadata = {
        "model_name": best_result["model"],
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_column": TARGET_COLUMN,
        "selection_metric": "f1_score",
        "metrics": best_result,
        "model_version": "v2",
    }

    with open(MODEL_METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"\nBest tuned model selected: {best_result['model']}")
    print(f"Best tuned model saved to: {BEST_MODEL_PATH}")
    print(f"Model metadata saved to: {MODEL_METADATA_PATH}")


if __name__ == "__main__":
    main()