import logging
from pathlib import Path

# Project root: backend/
BASE_DIR = Path(__file__).resolve().parents[2]

# Logs directory: Project Dumbo/logs
LOG_DIR = BASE_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "dumbo.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ProjectDumbo")
