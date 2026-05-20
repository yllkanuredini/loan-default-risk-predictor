import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, TARGET_COLUMN, RANDOM_STATE


def load_raw_data(file_name: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)
    return df


def inspect_data(df: pd.DataFrame) -> None:
    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nTarget distribution:")
    print(df[TARGET_COLUMN].value_counts())

    print("\nTarget distribution percentage:")
    print(df[TARGET_COLUMN].value_counts(normalize=True) * 100)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "LoanID" in df.columns:
        df = df.drop(columns=["LoanID"])

    df = df.drop_duplicates()

    return df


def split_data(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=y
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=RANDOM_STATE,
        stratify=y_temp
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def save_processed_data(df: pd.DataFrame, file_name: str) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DATA_DIR / file_name
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    df = load_raw_data("Loan_default.csv")

    inspect_data(df)

    cleaned_df = clean_data(df)

    print("\nCleaned dataset shape:")
    print(cleaned_df.shape)

    save_processed_data(cleaned_df, "loan_default_cleaned.csv")

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(cleaned_df)

    train_df = X_train.copy()
    train_df[TARGET_COLUMN] = y_train

    val_df = X_val.copy()
    val_df[TARGET_COLUMN] = y_val

    test_df = X_test.copy()
    test_df[TARGET_COLUMN] = y_test

    print("\nTrain shape:", train_df.shape)
    print("Validation shape:", val_df.shape)
    print("Test shape:", test_df.shape)

    print("\nTrain target distribution:")
    print(train_df[TARGET_COLUMN].value_counts(normalize=True) * 100)

    print("\nValidation target distribution:")
    print(val_df[TARGET_COLUMN].value_counts(normalize=True) * 100)

    print("\nTest target distribution:")
    print(test_df[TARGET_COLUMN].value_counts(normalize=True) * 100)

    save_processed_data(train_df, "train.csv")
    save_processed_data(val_df, "validation.csv")
    save_processed_data(test_df, "test.csv")