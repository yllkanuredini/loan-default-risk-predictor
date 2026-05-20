from pathlib import Path

# Main project directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

# Log paths
LOGS_DIR = BASE_DIR / "logs"
PREDICTION_LOG_PATH = LOGS_DIR / "prediction.log"

# Model paths
MODELS_DIR = BASE_DIR / "models"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
BEST_MODEL_PATH = MODELS_DIR / "best_model.joblib"
MODEL_METADATA_PATH = MODELS_DIR / "model_metadata.json"

# Reports paths
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_DIR = REPORTS_DIR / "metrics"

# Database paths
DATABASE_DIR = BASE_DIR / "database"
QUERIES_DIR = DATABASE_DIR / "queries"

# Default random seed
RANDOM_STATE = 42

# Target column
TARGET_COLUMN = "Default"