from sqlalchemy.orm import Session
from models import models

def get_user_by_username(db: Session, username: str):
    """Busca um usuário pelo nome de usuário."""
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()