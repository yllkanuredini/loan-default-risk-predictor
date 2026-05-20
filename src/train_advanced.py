import time
import joblib
import json
from datetime import datetime

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

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


def evaluate_model(model_name, model, X_val, y_val, training_time):
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    results = {
        "model": model_name,
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred, zero_division=0),
        "recall": recall_score(y_val, y_pred, zero_division=0),
        "f1_score": f1_score(y_val, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_val, y_proba),
        "training_time_seconds": training_time,
    }

    return results


def train_advanced_models():
    X_train, X_val, y_train, y_val, train_df = load_data()

    numerical_columns, categorical_columns = get_feature_columns(train_df)
    preprocessor = build_preprocessor(numerical_columns, categorical_columns)

    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight="balanced_subsample",
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),

        "Hist Gradient Boosting": HistGradientBoostingClassifier(
            max_iter=100,
            learning_rate=0.08,
            max_leaf_nodes=31,
            random_state=RANDOM_STATE
        ),

        "XGBoost": XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos_weight,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1
        ),

        "LightGBM": LGBMClassifier(
            n_estimators=300,
            max_depth=-1,
            learning_rate=0.05,
            num_leaves=31,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )
    }

    all_results = []

    best_pipeline = None
    best_result = None

    for model_name, classifier in models.items():
        print(f"\nTraining {model_name}...")

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", classifier)
            ]
        )

        start_time = time.time()
        pipeline.fit(X_train, y_train)
        training_time = time.time() - start_time

        results = evaluate_model(model_name, pipeline, X_val, y_val, training_time)
        all_results.append(results)

        print(f"{model_name} results:")
        for metric, value in results.items():
            if metric != "model":
                print(f"{metric}: {value:.4f}")

        if best_result is None or results["f1_score"] > best_result["f1_score"]:
            best_result = results
            best_pipeline = pipeline

    results_df = pd.DataFrame(all_results)

    print("\nAdvanced model comparison:")
    print(results_df)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    metrics_path = METRICS_DIR / "advanced_results.csv"
    results_df.to_csv(metrics_path, index=False)

    print(f"\nAdvanced results saved to: {metrics_path}")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_pipeline, BEST_MODEL_PATH)

    metadata = {
        "model_name": best_result["model"],
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_column": TARGET_COLUMN,
        "selection_metric": "f1_score",
        "metrics": best_result,
        "model_version": "v1"
    }

    with open(MODEL_METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"\nBest model selected: {best_result['model']}")
    print(f"Best model saved to: {BEST_MODEL_PATH}")
    print(f"Model metadata saved to: {MODEL_METADATA_PATH}")

    return results_df


if __name__ == "__main__":
    train_advanced_models()