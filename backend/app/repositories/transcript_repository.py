from app.repositories.base import BaseRepository


class TranscriptRepository(BaseRepository):
    def get_by_video_url(self, video_url: str):
        return self.db.query(self.model).filter(self.model.video_url == video_url).first()
