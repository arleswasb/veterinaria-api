from fastapi import APIRouter
from .routers import (
    atendimentos,
    auth,
    clinicas,
    pets,
    tutores,
    veterinarios,
)
from config import settings

# Roteador principal da API
router = APIRouter()

# Agrega os roteadores de cada entidade
router.include_router(auth.router)
router.include_router(clinicas.router)
router.include_router(veterinarios.router)
router.include_router(tutores.router)
router.include_router(pets.router)
router.include_router(atendimentos.router)

# O health check foi movido de main.py para cá para centralizar as rotas da API.
@router.get("/health", tags=["Health"])
def health_check():
    """Endpoint de verificação de saúde da API."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": settings.app_version,
    }

