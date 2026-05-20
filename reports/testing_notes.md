# Testing Notes

Basic tests were added with `pytest`.

Current test files:

- `tests/test_data_prep.py`
- `tests/test_predict.py`
- `tests/test_api.py`

The tests check that:

- `LoanID` is removed during cleaning
- duplicate rows are removed
- the saved model file exists
- predictions return the expected fields
- the FastAPI home endpoint works
- the prediction endpoint accepts valid input
- invalid numerical and categorical inputs are rejected

Current result:

- 8 tests passed

These tests provide basic confidence that the main project components work correctly.