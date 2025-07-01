from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão direta para PostgreSQL
# Para desenvolvimento, use esta URL diretamente
DATABASE_URL = "postgresql://postgres:postarl@localhost:5432/veterinaria_db"

# Criar engine com configurações específicas para PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_recycle=300,    # Recicla conexões a cada 5 minutos
    echo=False,          # Desabilitar log SQL temporariamente
    connect_args={
        "client_encoding": "utf8"  # Forçar encoding UTF-8
    }
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