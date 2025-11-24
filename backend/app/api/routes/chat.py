from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import SessionLocal
from app.schemas.chat import ChatCreate, ChatResponse, MessageCreate, MessageResponse, LLMRequestSchema, LLMResponseSchema
from app.schemas.user import UserResponse
from app.services.chat import chat_service
from app.services.llm_service import llm_service
from app.services.youtube import transcript_service
from app.api.routes.user import get_current_user

router = APIRouter(prefix="/api/chats", tags=["chats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):

    try:
        chat = chat_service.create_chat(
            db,
            user_id=current_user.user_id,
            transcript_id=chat_data.transcript_id
        )
        return ChatResponse.model_validate(chat)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating chat"
        )


@router.get("/", response_model=List[ChatResponse])
def get_user_chats(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        chats = chat_service.get_by_user_id(db, current_user.user_id)
        return [ChatResponse.model_validate(chat) for chat in chats]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching chats"
        )


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    if not chat_service.chat_belongs_to_user(db, chat_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this chat"
        )

    chat = chat_service.get_chat_with_messages(db, chat_id)

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    return ChatResponse.model_validate(chat)


@router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_message(
    chat_id: UUID,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    if not chat_service.chat_belongs_to_user(db, chat_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this chat"
        )

    try:
        message = chat_service.add_message(
            db,
            chat_id=chat_id,
            sender=message_data.sender,
            message_text=message_data.message_text
        )
        return MessageResponse.model_validate(message)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding message"
        )


@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    if not chat_service.chat_belongs_to_user(db, chat_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this chat"
        )

    chat = chat_service.get_chat_with_messages(db, chat_id)

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )

    return [MessageResponse.model_validate(msg) for msg in chat.messages]


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    if not chat_service.chat_belongs_to_user(db, chat_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this chat"
        )

    try:
        result = chat_service.delete_chat_with_messages(db, chat_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting chat"
        )


@router.get("/transcript/{transcript_id}", response_model=List[ChatResponse])
def get_chats_by_transcript(
    transcript_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        chats = chat_service.get_chats_by_transcript(db, transcript_id)
        user_chats = [chat for chat in chats if chat.user_id ==
                      current_user.user_id]
        return [ChatResponse.model_validate(chat) for chat in user_chats]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching chats"
        )


@router.post("/{chat_id}/llm", response_model=LLMResponseSchema)
async def send_message_to_llm(
    chat_id: UUID,
    request: LLMRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    if not chat_service.chat_belongs_to_user(db, chat_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this chat"
        )

    try:
        chat = chat_service.get_chat_with_messages(db, chat_id)

        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )

        chat_service.add_message(
            db,
            chat_id=chat_id,
            sender="user",
            message_text=request.user_message
        )

        transcript = None
        if chat.transcript_id:
            transcript = transcript_service.get_by_id(db, chat.transcript_id)

        if transcript and transcript.transcript_text:
            system_prompt = f"""You are a helpful AI assistant that helps users understand and discuss content from YouTube videos. Be concise, informative, and friendly.

Here is the transcript of the video being discussed:

{transcript.transcript_text}

Use this transcript to answer the user's questions accurately and provide relevant information from the video content."""
        else:
            system_prompt = "You are a helpful AI assistant that helps users understand and discuss content from YouTube videos. Be concise, informative, and friendly."

        messages = llm_service.format_chat_history(
            chat_messages=chat.messages,
            new_user_message=request.user_message,
            system_prompt=system_prompt
        )

        llm_response_text = llm_service.generate_response(
            provider=request.provider,
            messages=messages
        )

        chat_service.add_message(
            db,
            chat_id=chat_id,
            sender="llm",
            message_text=llm_response_text
        )

        return LLMResponseSchema(
            chat_id=chat_id,
            llm_message=llm_response_text
        )

    except ValueError as e:
        print(f"ValueError in LLM endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Exception in LLM endpoint: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing LLM request: {str(e)}"
        )
