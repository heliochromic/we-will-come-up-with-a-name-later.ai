from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID

from app.services.base import BaseService
from app.repositories.chat_repository import ChatRepository
from app.models.chat import Chat, Message
from app.schemas.chat import ChatCreate, MessageCreate


class ChatService(BaseService[Chat, ChatRepository]):
    def __init__(self):
        super().__init__(ChatRepository, Chat)

    def _validate_create(self, obj: Chat) -> None:
        if not obj.user_id:
            raise ValueError("User ID is required to create a chat")

    def _validate_update(self, obj: Chat, update_data: Dict[str, Any]) -> None:
        if "user_id" in update_data and update_data["user_id"] != obj.user_id:
            raise ValueError("Cannot change user_id of an existing chat")

    def _validate_delete(self, obj: Chat) -> None:
        pass

    def get_by_user_id(self, db: Session, user_id: UUID) -> List[Chat]:
        repo = self._get_repository(db)
        return repo.get_by_user_id(str(user_id))

    def create_chat(self, db: Session, user_id: UUID, transcript_id: Optional[UUID] = None) -> Chat:
        chat = Chat(
            user_id=user_id,
            transcript_id=transcript_id
        )

        return self.create(db, chat)

    def get_chat_with_messages(self, db: Session, chat_id: UUID) -> Optional[Chat]:
        chat = self.get_by_id(db, chat_id)
        if chat:
            if chat.messages:
                chat.messages.sort(key=lambda m: m.created_at)
        return chat

    def add_message(
        self,
        db: Session,
        chat_id: UUID,
        sender: str,
        message_text: str
    ) -> Message:
        chat = self.get_by_id(db, chat_id)
        if not chat:
            raise ValueError(f"Chat with ID {chat_id} not found")

        valid_senders = ['user', 'system', 'llm']
        if sender not in valid_senders:
            raise ValueError(
                f"Invalid sender. Must be one of: {', '.join(valid_senders)}")

        if not message_text or len(message_text.strip()) == 0:
            raise ValueError("Message text cannot be empty")

        message = Message(
            chat_id=chat_id,
            sender=sender,
            message_text=message_text
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def get_last_message(self, db: Session, chat_id: UUID) -> Optional[Message]:
        message = db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at.desc()).first()

        return message

    def delete_chat_with_messages(self, db: Session, chat_id: UUID) -> bool:
        return self.delete(db, chat_id)

    def count_messages(self, db: Session, chat_id: UUID) -> int:
        count = db.query(Message).filter(Message.chat_id == chat_id).count()
        return count

    def get_user_chat_count(self, db: Session, user_id: UUID) -> int:
        count = db.query(Chat).filter(Chat.user_id == user_id).count()
        return count

    def chat_belongs_to_user(self, db: Session, chat_id: UUID, user_id: UUID) -> bool:
        chat = self.get_by_id(db, chat_id)
        if not chat:
            return False
        return chat.user_id == user_id

    def get_chats_by_transcript(self, db: Session, transcript_id: UUID) -> List[Chat]:
        chats = db.query(Chat).filter(
            Chat.transcript_id == transcript_id
        ).order_by(Chat.created_at.desc()).all()

        return chats


chat_service = ChatService()
