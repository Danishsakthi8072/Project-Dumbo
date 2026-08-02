from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: UserCreate):
        existing_user = (
            self.db.query(User)
            .filter(
                (User.username == user.username) |
                (User.email == user.email)
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Username or email already exists.",
            )

        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password),
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
