from sqlalchemy.orm import Session
from models import models
from schemas import tutor as tutor_schema

def get_tutor(db: Session, tutor_id: int):
    """Busca um único tutor pelo ID."""
    return db.query(models.Tutor).filter(models.Tutor.id == tutor_id).first()

def get_tutores(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os tutores com paginação."""
    return db.query(models.Tutor).offset(skip).limit(limit).all()

def create_tutor(db: Session, tutor: tutor_schema.TutorCreate):
    """Cria um novo tutor no banco de dados."""
    db_tutor = models.Tutor(**tutor.model_dump())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

def update_tutor(db: Session, tutor_id: int, tutor: tutor_schema.TutorUpdate):
    """Atualiza um tutor existente."""
    db_tutor = get_tutor(db, tutor_id)
    if db_tutor:
        update_data = tutor.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tutor, key, value)
        db.commit()
        db.refresh(db_tutor)
    return db_tutor

def delete_tutor(db: Session, tutor_id: int):
    """Deleta um tutor do banco de dados."""
    db_tutor = get_tutor(db, tutor_id)
    if db_tutor:
        db.delete(db_tutor)
        db.commit()
    return db_tutor