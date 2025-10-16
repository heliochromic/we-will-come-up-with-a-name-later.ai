from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def get_by_email(self, email: str):
        return self.db.query(self.model).filter(self.model.email.is_(email)).first()

