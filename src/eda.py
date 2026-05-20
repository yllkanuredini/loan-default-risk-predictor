import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import PROCESSED_DATA_DIR, FIGURES_DIR, TARGET_COLUMN


def load_cleaned_data():
    file_path = PROCESSED_DATA_DIR / "loan_default_cleaned.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def save_plot(file_name: str):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / file_name
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved figure: {output_path}")


def plot_target_distribution(df):
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x=TARGET_COLUMN)
    plt.title("Target Distribution")
    plt.xlabel("Default")
    plt.ylabel("Number of Records")
    save_plot("target_distribution.png")


def plot_numerical_distributions(df):
    numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    numerical_columns = [col for col in numerical_columns if col != TARGET_COLUMN]

    for column in numerical_columns:
        plt.figure(figsize=(7, 4))
        sns.histplot(df[column], bins=30, kde=True)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        save_plot(f"distribution_{column}.png")


def plot_categorical_default_rates(df):
    categorical_columns = df.select_dtypes(include=["object", "string"]).columns.tolist()

    for column in categorical_columns:
        default_rate = (
            df.groupby(column)[TARGET_COLUMN]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        plt.figure(figsize=(8, 4))
        sns.barplot(data=default_rate, x=column, y=TARGET_COLUMN)
        plt.title(f"Default Rate by {column}")
        plt.xlabel(column)
        plt.ylabel("Default Rate")
        plt.xticks(rotation=30, ha="right")
        save_plot(f"default_rate_by_{column}.png")


def plot_correlation_matrix(df):
    numerical_df = df.select_dtypes(include=["int64", "float64"])

    plt.figure(figsize=(10, 7))
    sns.heatmap(numerical_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix")
    save_plot("correlation_matrix.png")


def main():
    df = load_cleaned_data()

    print("\nRunning EDA...")
    print(f"Dataset shape: {df.shape}")

    plot_target_distribution(df)
    plot_numerical_distributions(df)
    plot_categorical_default_rates(df)
    plot_correlation_matrix(df)

    print("\nEDA completed successfully.")


if __name__ == "__main__":
    main()