from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from uuid import UUID
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import re

from app.services.base import BaseService
from app.repositories.transcript_repository import TranscriptRepository
from app.models.transcript import Transcript
from app.schemas.transcript import TranscriptBase, TranscriptCreate, TranscriptResponse


class TranscriptService(BaseService[Transcript, TranscriptRepository]):
    def __init__(self):
        super().__init__(TranscriptRepository, Transcript)

    def _validate_create(self, obj: Transcript) -> None:
        if not obj.video_url:
            raise ValueError("Video URL is required")

        if not obj.transcript_text or not obj.transcript_text.strip():
            raise ValueError("Transcript text cannot be empty")

        if obj.language and obj.language.lower() in ['ru', 'rus', 'russian']:
            raise ValueError(
                "Kill yourself, Russian language transcripts are not supported")

        if obj.duration is not None and obj.duration <= 0:
            raise ValueError("Duration must be a positive number")

    def _validate_update(self, obj: Transcript, update_data: Dict[str, Any]) -> None:
        if 'video_url' in update_data and not update_data['video_url']:
            raise ValueError("Video URL cannot be empty")

        if 'transcript_text' in update_data:
            if not update_data['transcript_text'] or not update_data['transcript_text'].strip():
                raise ValueError("Transcript text cannot be empty")

        if 'language' in update_data:
            language = update_data['language']
            if language and language.lower() in ['ru', 'rus', 'russian']:
                raise ValueError(
                    "Kill yourself, Russian language transcripts are not supported")

        if 'duration' in update_data:
            duration = update_data['duration']
            if duration is not None and duration <= 0:
                raise ValueError("Duration must be a positive number")

    def _validate_delete(self, obj: Transcript) -> None:
        pass

    def get_by_url(self, db: Session, url: str) -> Optional[Transcript]:
        repo = self._get_repository(db)
        return repo.get_by_video_url(video_url=url)

    def _extract_video_id(self, url: str) -> str:
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        raise ValueError(f"Could not extract video ID from URL: {url}")

    def _fetch_youtube_url(self, url: str) -> Dict[str, Any]:
        try:
            video_id = self._extract_video_id(url)

            ytt_api = YouTubeTranscriptApi()

            transcript_data = ytt_api.fetch(video_id, languages=['en'])

            transcript_text = " ".join(
                [entry.text for entry in transcript_data.snippets])

            duration = None
            if transcript_data.snippets:
                last_entry = transcript_data.snippets[-1]
                duration = last_entry.start + last_entry.duration

            language = transcript_data.language_code if hasattr(
                transcript_data, 'language_code') else 'en'

            return {
                'transcript_text': transcript_text,
                'language': language,
                'duration': duration
            }

        except TranscriptsDisabled:
            raise ValueError(f"Transcripts are disabled for video: {url}")
        except NoTranscriptFound:
            raise ValueError(f"No transcript found for video: {url}")
        except VideoUnavailable:
            raise ValueError(f"Video is unavailable: {url}")
        except Exception as e:
            raise ValueError(f"Error fetching transcript: {str(e)}")

    def get_transcript(self, db: Session, transcript_data: TranscriptCreate) -> Transcript:
        existing_transcript = self.get_by_url(
            db, str(transcript_data.video_url))
        if existing_transcript:
            return existing_transcript

        transcript_info = self._fetch_youtube_url(
            str(transcript_data.video_url))

        transcript = Transcript(
            video_url=str(transcript_data.video_url),
            transcript_text=transcript_info['transcript_text'],
            language=transcript_info['language'],
            duration=transcript_info['duration']
        )

        repo = self._get_repository(db)
        return repo.create(obj=transcript)


transcript_service = TranscriptService()
