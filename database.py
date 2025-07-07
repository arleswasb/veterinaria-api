from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Usar a URL de banco de dados das configurações
DATABASE_URL = settings.effective_database_url

# Criar engine com configurações específicas para PostgreSQL/SQLite
engine_kwargs = {
    "pool_pre_ping": True,  # Verifica conexões antes de usar
    "echo": False,          # Desabilitar log SQL temporariamente
}

# Configurações específicas para PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    engine_kwargs.update({
        "pool_recycle": 300,    # Recicla conexões a cada 5 minutos
        "connect_args": {
            "client_encoding": "utf8"  # Forçar encoding UTF-8
        }
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()