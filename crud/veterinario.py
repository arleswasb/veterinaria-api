"""
CRUD operations for Veterinario model.
"""
from sqlalchemy.orm import Session
from models import models
from services import schemas


def get_veterinario(db: Session, veterinario_id: int):
    """Busca um único veterinário pelo ID."""
    return db.query(models.Veterinario).filter(models.Veterinario.id == veterinario_id).first()


def get_veterinarios(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os veterinários com paginação."""
    return db.query(models.Veterinario).offset(skip).limit(limit).all()


def get_veterinarios_by_clinica(db: Session, clinica_id: int):
    """Busca veterinários de uma clínica específica."""
    return db.query(models.Veterinario).filter(models.Veterinario.clinica_id == clinica_id).all()


def create_veterinario(db: Session, veterinario: schemas.VeterinarioCreate):
    """Cria um novo veterinário."""
    db_veterinario = models.Veterinario(**veterinario.dict())
    db.add(db_veterinario)
    db.commit()
    db.refresh(db_veterinario)
    return db_veterinario


def update_veterinario(db: Session, veterinario_id: int, veterinario: schemas.VeterinarioCreate):
    """Atualiza um veterinário existente."""
    db_veterinario = get_veterinario(db, veterinario_id)
    if db_veterinario:
        for key, value in veterinario.dict().items():
            setattr(db_veterinario, key, value)
        db.commit()
        db.refresh(db_veterinario)
    return db_veterinario


def delete_veterinario(db: Session, veterinario_id: int):
    """Deleta um veterinário."""
    db_veterinario = get_veterinario(db, veterinario_id)
    if db_veterinario:
        db.delete(db_veterinario)
        db.commit()
    return db_veterinario
