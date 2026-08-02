from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

users = db.query(User).all()

if not users:
    print("No users found.")
else:
    print("Users:")
    for user in users:
        print(
            f"ID={user.id} | Username={user.username} | Email={user.email}"
        )

db.close()
