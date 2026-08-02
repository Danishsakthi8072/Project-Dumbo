from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):
        message = Conversation(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.conversation_id == conversation_id
            )
            .order_by(Conversation.id)
            .all()
        )

    def clear(
        self,
        conversation_id: str,
    ):
        (
            self.db.query(Conversation)
            .filter(
                Conversation.conversation_id == conversation_id
            )
            .delete()
        )

        self.db.commit()