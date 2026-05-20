# Threshold Strategy

The model returns a default probability, and the threshold decides when that probability becomes a `Default` prediction.

Several thresholds were tested on the test set.

Best balanced threshold:

- Threshold: 0.50
- Accuracy: 0.8126
- Precision: 0.3029
- Recall: 0.4719
- F1-score: 0.3690

A lower threshold, such as 0.25, gives very high recall but creates many false positives. This means it catches most default cases but wrongly flags many good borrowers.

A higher threshold, such as 0.60, improves precision but misses more real default cases.

For this project, threshold 0.50 was selected because it gave the best F1-score and the best balance between catching defaults and avoiding too many false alarms.