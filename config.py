import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configurações do banco de dados
    # Para desenvolvimento local: SQLite
    # Para produção: PostgreSQL
    database_url: str = "sqlite:///./veterinaria.db"
    
    # Configurações PostgreSQL (quando necessário)
    postgres_user: str = "postgres"
    postgres_password: str = "postarl"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "veterinaria_db"
    
    # Configurações da aplicação
    app_name: str = "API de Gerenciamento de Clínicas Veterinárias"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"  # development, production
    
    @property
    def postgres_url(self) -> str:
        """Constrói a URL do PostgreSQL a partir das configurações."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def effective_database_url(self) -> str:
        """Retorna a URL efetiva do banco baseada no ambiente."""
        if self.environment == "production" or self.database_url.startswith("postgresql"):
            return self.postgres_url
        return self.database_url
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
