# Logging Notes

Basic logging was added to track prediction activity.

The reusable logger is defined in `src/utils.py`, and prediction logs are saved to `logs/prediction.log`.

The prediction script logs:

- when the model is loaded
- when a prediction is completed
- the prediction label
- the default probability
- the risk category

Logging makes the project easier to debug and more production-ready.