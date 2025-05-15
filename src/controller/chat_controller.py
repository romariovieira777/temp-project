from fastapi import APIRouter
from src.services.chat_service import ChatService

router = APIRouter()

@router.get("/buscar/nome/{nome}/telefone/{telefone}")
async def buscar(nome: str, telefone: str):
    return ChatService.executar(nome=nome, telefone=telefone)
