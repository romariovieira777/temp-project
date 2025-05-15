from fastapi import APIRouter
from src.controller import chat_controller
router = APIRouter()

router.include_router(chat_controller.router, prefix='/api/v1/myside', tags=['Busca'])