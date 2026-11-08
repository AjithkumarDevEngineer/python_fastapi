from fastapi import FastAPI
from fastapi_ai_chat.config import settings
from fastapi_ai_chat.routers import chat_router

app= FastAPI(title=settings.app_name, version="1.0.0")

app.include_router(chat_router.router)