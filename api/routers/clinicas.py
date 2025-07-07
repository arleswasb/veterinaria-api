from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import clinica as clinica_schema
from crud import clinica as clinica_crud
from services.auth import get_current_active_user
from schemas import usuario as usuario_schema

router = APIRouter(
    prefix="/clinicas",
    tags=["Clínicas"],
    responses={404: {"description": "Clínica não encontrada"}},
    # Adiciona a dependência de autenticação a TODAS as rotas deste roteador
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=clinica_schema.Clinica, status_code=status.HTTP_201_CREATED)
def create_clinica(clinica: clinica_schema.ClinicaCreate, db: Session = Depends(get_db)):
    """Cria uma nova clínica."""
    return clinica_crud.create_clinica(db=db, clinica=clinica)

@router.get("/", response_model=List[clinica_schema.Clinica])
def read_clinicas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as clínicas."""
    clinicas = clinica_crud.get_clinicas(db, skip=skip, limit=limit)
    return clinicas

@router.get("/{clinica_id}", response_model=clinica_schema.Clinica)
def read_clinica(clinica_id: int, db: Session = Depends(get_db)):
    """Busca os detalhes de uma clínica específica."""
    db_clinica = clinica_crud.get_clinica(db, clinica_id=clinica_id)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return db_clinica

@router.put("/{clinica_id}", response_model=clinica_schema.Clinica)
def update_clinica(clinica_id: int, clinica: clinica_schema.ClinicaUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de uma clínica."""
    db_clinica = clinica_crud.update_clinica(db, clinica_id=clinica_id, clinica=clinica)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return db_clinica

@router.delete("/{clinica_id}", response_model=clinica_schema.Clinica)
def delete_clinica(clinica_id: int, db: Session = Depends(get_db)):
    """Remove uma clínica do sistema."""
    db_clinica = clinica_crud.delete_clinica(db, clinica_id=clinica_id)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return db_clinica