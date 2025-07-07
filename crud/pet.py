from sqlalchemy.orm import Session
from models import models
from schemas import pet as pet_schema

def get_pet(db: Session, pet_id: int):
    """Busca um único pet pelo ID."""
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def get_pets(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os pets com paginação."""
    return db.query(models.Pet).offset(skip).limit(limit).all()

def create_pet(db: Session, pet: pet_schema.PetCreate):
    """Cria um novo pet no banco de dados."""
    db_pet = models.Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def update_pet(db: Session, pet_id: int, pet: pet_schema.PetUpdate):
    """Atualiza um pet existente."""
    db_pet = get_pet(db, pet_id)
    if db_pet:
        update_data = pet.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_pet, key, value)
        db.commit()
        db.refresh(db_pet)
    return db_pet

def delete_pet(db: Session, pet_id: int):
    """Deleta um pet do banco de dados."""
    db_pet = get_pet(db, pet_id)
    if db_pet:
        db.delete(db_pet)
        db.commit()
    return db_pet