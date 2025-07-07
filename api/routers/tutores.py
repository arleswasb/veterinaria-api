from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import tutor as tutor_schema
from crud import tutor as tutor_crud
from services.auth import get_current_active_user

router = APIRouter(
    prefix="/tutores",
    tags=["Tutores"],
    responses={404: {"description": "Tutor não encontrado"}},
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=tutor_schema.Tutor, status_code=status.HTTP_201_CREATED)
def create_tutor(tutor: tutor_schema.TutorCreate, db: Session = Depends(get_db)):
    """Cria um novo tutor."""
    return tutor_crud.create_tutor(db=db, tutor=tutor)

@router.get("/", response_model=List[tutor_schema.Tutor])
def read_tutores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os tutores."""
    tutores = tutor_crud.get_tutores(db, skip=skip, limit=limit)
    return tutores

@router.get("/{tutor_id}", response_model=tutor_schema.Tutor)
def read_tutor(tutor_id: int, db: Session = Depends(get_db)):
    """Busca os detalhes de um tutor específico."""
    db_tutor = tutor_crud.get_tutor(db, tutor_id=tutor_id)
    if db_tutor is None:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return db_tutor

@router.put("/{tutor_id}", response_model=tutor_schema.Tutor)
def update_tutor(tutor_id: int, tutor: tutor_schema.TutorUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de um tutor."""
    db_tutor = tutor_crud.update_tutor(db, tutor_id=tutor_id, tutor=tutor)
    if db_tutor is None:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return db_tutor

@router.delete("/{tutor_id}", response_model=tutor_schema.Tutor)
def delete_tutor(tutor_id: int, db: Session = Depends(get_db)):
    """Remove um tutor do sistema."""
    db_tutor = tutor_crud.delete_tutor(db, tutor_id=tutor_id)
    if db_tutor is None:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return db_tutor