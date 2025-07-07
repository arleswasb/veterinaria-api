# veterinaria/main.py

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from api import routes
from config import settings
from api import exception_handlers
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Sistema para gerenciar atendimentos, clínicas, tutores, pets e veterinários.",
    version=settings.app_version,
    debug=settings.debug,
    # Configura a documentação para usar o prefixo /api
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"  # Removido o prefixo /api para evitar conflitos
)

# Middleware de logging (opcional para debugging)
if settings.debug:
    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"📡 {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"📤 Status: {response.status_code}")
        return response

# Adiciona os handlers de exceção customizados
app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
app.add_exception_handler(IntegrityError, exception_handlers.integrity_error_handler)

# Inclui o roteador da API com o prefixo /api
app.include_router(routes.router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz da API com informações básicas."""
    return {
        "message": "Bem-vindo à API de Clínicas Veterinárias. Acesse /docs para ver a documentação.",
        "version": settings.app_version,
        "docs_url": "/docs",
        "health_check": "/api/health",
    }