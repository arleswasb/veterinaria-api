from sqlalchemy.orm import Session
from models import models
from schemas import clinica as clinica_schema

def get_clinica(db: Session, clinica_id: int):
    """Busca uma única clínica pelo ID."""
    return db.query(models.Clinica).filter(models.Clinica.id == clinica_id).first()

def get_clinicas(db: Session, skip: int = 0, limit: int = 100):
    """Busca todas as clínicas com paginação."""
    return db.query(models.Clinica).offset(skip).limit(limit).all()

def create_clinica(db: Session, clinica: clinica_schema.ClinicaCreate):
    """Cria uma nova clínica no banco de dados."""
    db_clinica = models.Clinica(**clinica.model_dump())
    db.add(db_clinica)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

def update_clinica(db: Session, clinica_id: int, clinica: clinica_schema.ClinicaUpdate):
    """Atualiza uma clínica existente."""
    db_clinica = get_clinica(db, clinica_id)
    if db_clinica:
        update_data = clinica.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_clinica, key, value)
        db.commit()
        db.refresh(db_clinica)
    return db_clinica

def delete_clinica(db: Session, clinica_id: int):
    """Deleta uma clínica do banco de dados."""
    db_clinica = get_clinica(db, clinica_id)
    if db_clinica:
        db.delete(db_clinica)
        db.commit()
    return db_clinica