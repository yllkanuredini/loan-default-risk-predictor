import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.config import TARGET_COLUMN


def get_feature_columns(df: pd.DataFrame):
    X = df.drop(columns=[TARGET_COLUMN])

    numerical_columns = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_columns = X.select_dtypes(include=["object", "string"]).columns.tolist()

    return numerical_columns, categorical_columns


def build_preprocessor(numerical_columns, categorical_columns):
    numerical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_pipeline, numerical_columns),
            ("cat", categorical_pipeline, categorical_columns),
        ]
    )

    return preprocessor