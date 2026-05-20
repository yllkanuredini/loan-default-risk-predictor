import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from src.config import PROCESSED_DATA_DIR, TARGET_COLUMN, RANDOM_STATE, METRICS_DIR
from src.features import get_feature_columns, build_preprocessor


def load_data():
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "validation.csv")

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    X_val = val_df.drop(columns=[TARGET_COLUMN])
    y_val = val_df[TARGET_COLUMN]

    return X_train, X_val, y_train, y_val, train_df


def evaluate_model(model_name, model, X_val, y_val):
    y_pred = model.predict(X_val)
    y_proba = model.predict_proba(X_val)[:, 1]

    results = {
        "model": model_name,
        "accuracy": accuracy_score(y_val, y_pred),
        "precision": precision_score(y_val, y_pred, zero_division=0),
        "recall": recall_score(y_val, y_pred, zero_division=0),
        "f1_score": f1_score(y_val, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_val, y_proba),
    }

    return results


def train_baseline_models():
    X_train, X_val, y_train, y_val, train_df = load_data()

    numerical_columns, categorical_columns = get_feature_columns(train_df)
    preprocessor = build_preprocessor(numerical_columns, categorical_columns)

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=6,
            class_weight="balanced",
            random_state=RANDOM_STATE
        )
    }

    all_results = []

    for model_name, classifier in models.items():
        print(f"\nTraining {model_name}...")

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", classifier)
            ]
        )

        pipeline.fit(X_train, y_train)

        results = evaluate_model(model_name, pipeline, X_val, y_val)
        all_results.append(results)

        print(f"{model_name} results:")
        for metric, value in results.items():
            if metric != "model":
                print(f"{metric}: {value:.4f}")

    results_df = pd.DataFrame(all_results)

    print("\nBaseline model comparison:")
    print(results_df)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    metrics_path = METRICS_DIR / "baseline_results.csv"
    results_df.to_csv(metrics_path, index=False)

    print(f"\nBaseline results saved to: {metrics_path}")

    return results_df


if __name__ == "__main__":
    train_baseline_models()