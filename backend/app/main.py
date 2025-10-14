from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="YouTube LLM Agent API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
# transcript_router = APIRouter(prefix="/api/transcripts", tags=["transcripts"])
# chat_router = APIRouter(prefix="/api/chats", tags=["chats"])

# app.include_router(auth_router)
# app.include_router(transcript_router)
# app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "YouTube LLM Agent API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
