from typing import List

from app.models.chat import Chat
from app.repositories.base import BaseRepository


class ChatRepository(BaseRepository):
    def get_by_user_id(self, user_id: str) -> List[Chat]:
        return self.db.query(self.model).filter(self.model.user_id.is_(user_id)).all()