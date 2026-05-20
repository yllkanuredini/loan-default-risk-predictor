import pandas as pd

from src.config import PROCESSED_DATA_DIR, TARGET_COLUMN
from src.features import get_feature_columns, build_preprocessor


def main():
    train_path = PROCESSED_DATA_DIR / "train.csv"

    train_df = pd.read_csv(train_path)

    X_train = train_df.drop(columns=[TARGET_COLUMN])
    y_train = train_df[TARGET_COLUMN]

    numerical_columns, categorical_columns = get_feature_columns(train_df)

    print("\nNumerical columns:")
    print(numerical_columns)

    print("\nCategorical columns:")
    print(categorical_columns)

    preprocessor = build_preprocessor(numerical_columns, categorical_columns)

    X_train_transformed = preprocessor.fit_transform(X_train)

    print("\nOriginal training shape:")
    print(X_train.shape)

    print("\nTransformed training shape:")
    print(X_train_transformed.shape)

    print("\nTarget shape:")
    print(y_train.shape)


if __name__ == "__main__":
    main()