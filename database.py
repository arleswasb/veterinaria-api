from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# URL de conexão dinâmica baseada na configuração
DATABASE_URL = settings.effective_database_url

# Configurações específicas por tipo de banco
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}  # Necessário para SQLite
    )
else:
    # PostgreSQL
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verifica conexões antes de usar
        pool_recycle=300,    # Recicla conexões a cada 5 minutos
        echo=settings.debug  # Log de SQL apenas em debug
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()