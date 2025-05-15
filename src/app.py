from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.router.router import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """
        Retorna uma mensagem de boas-vindas
    """
    return {
        "message": "Welcome MySide API",
        "version": "0.1.0"
    }
app.include_router(router=router)  