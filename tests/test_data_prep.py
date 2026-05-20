import pandas as pd

from src.data_prep import clean_data


def test_clean_data_removes_loan_id():
    sample_df = pd.DataFrame(
        {
            "LoanID": ["A1", "B2"],
            "Age": [30, 45],
            "Income": [50000, 80000],
            "Default": [0, 1],
        }
    )

    cleaned_df = clean_data(sample_df)

    assert "LoanID" not in cleaned_df.columns


def test_clean_data_removes_duplicates():
    sample_df = pd.DataFrame(
        {
            "LoanID": ["A1", "A1"],
            "Age": [30, 30],
            "Income": [50000, 50000],
            "Default": [0, 0],
        }
    )

    cleaned_df = clean_data(sample_df)

    assert len(cleaned_df) == 1