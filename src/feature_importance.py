import pandas as pd
import matplotlib.pyplot as plt
import joblib

from src.config import BEST_MODEL_PATH, FIGURES_DIR, METRICS_DIR


def load_model():
    if not BEST_MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {BEST_MODEL_PATH}")

    return joblib.load(BEST_MODEL_PATH)


def get_feature_names(preprocessor):
    numerical_features = preprocessor.named_transformers_["num"].get_feature_names_out()
    categorical_features = preprocessor.named_transformers_["cat"].get_feature_names_out()

    all_features = list(numerical_features) + list(categorical_features)

    cleaned_features = [
        feature.replace("num__", "").replace("cat__", "")
        for feature in all_features
    ]

    return cleaned_features


def main():
    model_pipeline = load_model()

    preprocessor = model_pipeline.named_steps["preprocessor"]
    classifier = model_pipeline.named_steps["classifier"]

    feature_names = get_feature_names(preprocessor)
    importances = classifier.feature_importances_

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    ).sort_values(by="importance", ascending=False)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = METRICS_DIR / "feature_importance.csv"
    importance_df.to_csv(csv_path, index=False)

    print("\nTop 15 important features:")
    print(importance_df.head(15))

    top_features = importance_df.head(15).sort_values(by="importance")

    plt.figure(figsize=(10, 6))
    plt.barh(top_features["feature"], top_features["importance"])
    plt.title("Top 15 Feature Importances")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()

    figure_path = FIGURES_DIR / "feature_importance.png"
    plt.savefig(figure_path, dpi=300)
    plt.close()

    print(f"\nFeature importance saved to: {csv_path}")
    print(f"Feature importance chart saved to: {figure_path}")


if __name__ == "__main__":
    main()