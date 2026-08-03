from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import Base, engine

# Import ALL models so SQLAlchemy registers every table
from app.models.user import User
from app.models.conversation import Conversation
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

db_path = Path(engine.url.database)

db_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

Base.metadata.create_all(bind=engine)

print(f"Database ready: {db_path}")
print("Tables:")

for table in Base.metadata.tables:
    print(f" - {table}")