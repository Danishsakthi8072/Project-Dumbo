from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

user = User(
    username="admin",
    email="admin@dumbo.local",
    password_hash="dummy_hash",
)

db.add(user)
db.commit()
db.refresh(user)

print("User created successfully!")
print(f"ID: {user.id}")
print(f"Username: {user.username}")
print(f"Email: {user.email}")

db.close()
