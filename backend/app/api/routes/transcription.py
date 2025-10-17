from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import SessionLocal
from app.schemas.transcript import TranscriptCreate, TranscriptResponse
from app.schemas.user import UserResponse
from app.services.youtube import transcript_service
from app.api.routes.user import get_current_user

router = APIRouter(prefix="/api/transcripts", tags=["transcripts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TranscriptResponse, status_code=status.HTTP_201_CREATED)
def create_transcript(
    transcript_data: TranscriptCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        transcript = transcript_service.get_transcript(db, transcript_data)
        return TranscriptResponse.from_orm(transcript)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching transcript: {str(e)}"
        )


@router.get("/{transcript_id}", response_model=TranscriptResponse)
def get_transcript_by_id(
    transcript_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    transcript = transcript_service.get_by_id(db, transcript_id)

    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found"
        )

    return TranscriptResponse.from_orm(transcript)


@router.get("/", response_model=List[TranscriptResponse])
def get_all_transcripts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        transcripts = transcript_service.get_all(db, skip=skip, limit=limit)
        return [TranscriptResponse.from_orm(t) for t in transcripts]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching transcripts"
        )


@router.delete("/{transcript_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transcript(
    transcript_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        result = transcript_service.delete(db, transcript_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcript not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting transcript"
        )
