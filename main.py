# veterinaria/main.py

from fastapi import FastAPI
from api import routes
from database import engine
from models import models
from config import settings

# Esta linha cria as tabelas no banco de dados com base nos seus modelos SQLAlchemy
# É executada apenas uma vez quando a aplicação inicia
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Aviso: Não foi possível criar as tabelas automaticamente: {e}")
    print("Certifique-se de que o banco de dados está configurado corretamente.")

app = FastAPI(
    title=settings.app_name,
    description="Sistema para gerenciar atendimentos, clínicas, tutores, pets e veterinários.",
    version=settings.app_version,
    debug=settings.debug,
    # Configura a documentação para usar o prefixo /api
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json" 
)

# Inclui o roteador da API com o prefixo /api
app.include_router(routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Clínicas Veterinárias. Acesse /docs para ver a documentação."}