from fastapi import HTTPException

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(self):
        return self.repository.get_all()

    def create_user(self, user: UserCreate):
        return self.repository.create(user)

    def login(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        return {
            "access_token": create_access_token(
                {
                    "sub": str(user.id),
                    "email": user.email,
                }
            ),
            "token_type": "bearer",
        }

    def get_current_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found.",
            )

        return user
