from sqlalchemy.orm import Session
from models import models
from schemas import atendimento as atendimento_schema

def get_atendimento(db: Session, atendimento_id: int):
    """Busca um único atendimento pelo ID."""
    return db.query(models.Atendimento).filter(models.Atendimento.id == atendimento_id).first()

def get_atendimentos(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os atendimentos com paginação."""
    return db.query(models.Atendimento).offset(skip).limit(limit).all()

def create_atendimento(db: Session, atendimento: atendimento_schema.AtendimentoCreate):
    """Cria um novo atendimento no banco de dados."""
    db_atendimento = models.Atendimento(**atendimento.model_dump())
    db.add(db_atendimento)
    db.commit()
    db.refresh(db_atendimento)
    return db_atendimento

def update_atendimento(db: Session, atendimento_id: int, atendimento: atendimento_schema.AtendimentoUpdate):
    """Atualiza um atendimento existente."""
    db_atendimento = get_atendimento(db, atendimento_id)
    if db_atendimento:
        update_data = atendimento.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_atendimento, key, value)
        db.commit()
        db.refresh(db_atendimento)
    return db_atendimento

def delete_atendimento(db: Session, atendimento_id: int):
    """Deleta um atendimento do banco de dados."""
    db_atendimento = get_atendimento(db, atendimento_id)
    if db_atendimento:
        db.delete(db_atendimento)
        db.commit()
    return db_atendimento