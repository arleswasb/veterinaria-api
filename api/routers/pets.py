from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import pet as pet_schema
from crud import pet as pet_crud, tutor as tutor_crud
from services.auth import get_current_active_user

router = APIRouter(
    prefix="/pets",
    tags=["Pets"],
    responses={404: {"description": "Pet não encontrado"}},
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=pet_schema.Pet, status_code=status.HTTP_201_CREATED)
def create_pet(pet: pet_schema.PetCreate, db: Session = Depends(get_db)):
    """Cria um novo pet para um tutor."""
    # Validação de negócio: verificar se o tutor existe
    db_tutor = tutor_crud.get_tutor(db, tutor_id=pet.tutor_id)
    if not db_tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tutor com id {pet.tutor_id} não encontrado."
        )
    return pet_crud.create_pet(db=db, pet=pet)

@router.get("/", response_model=List[pet_schema.Pet])
def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os pets."""
    pets = pet_crud.get_pets(db, skip=skip, limit=limit)
    return pets

@router.get("/{pet_id}", response_model=pet_schema.Pet)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    """Busca os detalhes de um pet específico."""
    db_pet = pet_crud.get_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return db_pet

@router.put("/{pet_id}", response_model=pet_schema.Pet)
def update_pet(pet_id: int, pet: pet_schema.PetUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de um pet."""
    db_pet = pet_crud.update_pet(db, pet_id=pet_id, pet=pet)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return db_pet

@router.delete("/{pet_id}", response_model=pet_schema.Pet)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """Remove um pet do sistema."""
    db_pet = pet_crud.delete_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return db_pet