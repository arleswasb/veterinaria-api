from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import atendimento as atendimento_schema
from crud import atendimento as atendimento_crud
from services import auth as auth_service, atendimento_service

router = APIRouter(
    prefix="/atendimentos",
    tags=["Atendimentos"],
    responses={404: {"description": "Atendimento não encontrado"}},
    # Adiciona a dependência de autenticação a TODAS as rotas deste roteador
    dependencies=[Depends(auth_service.get_current_active_user)]
)

@router.post("/", response_model=atendimento_schema.Atendimento, status_code=status.HTTP_201_CREATED)
def create_atendimento(atendimento: atendimento_schema.AtendimentoCreate, db: Session = Depends(get_db)):
    """Cria um novo registro de atendimento."""
    return atendimento_service.create_new_atendimento(db=db, atendimento=atendimento)

@router.get("/", response_model=List[atendimento_schema.Atendimento])
def read_atendimentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os atendimentos."""
    atendimentos = atendimento_crud.get_atendimentos(db, skip=skip, limit=limit)
    return atendimentos

@router.get("/{atendimento_id}", response_model=atendimento_schema.Atendimento)
def read_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    """Busca os detalhes de um atendimento específico."""
    db_atendimento = atendimento_crud.get_atendimento(db, atendimento_id=atendimento_id)
    if db_atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    return db_atendimento

@router.put("/{atendimento_id}", response_model=atendimento_schema.Atendimento)
def update_atendimento(atendimento_id: int, atendimento: atendimento_schema.AtendimentoUpdate, db: Session = Depends(get_db)):
    """Atualiza a descrição de um atendimento."""
    db_atendimento = atendimento_crud.update_atendimento(db, atendimento_id=atendimento_id, atendimento=atendimento)
    if db_atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    return db_atendimento

@router.delete("/{atendimento_id}", response_model=atendimento_schema.Atendimento)
def delete_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    """Remove um registro de atendimento do sistema."""
    db_atendimento = atendimento_crud.delete_atendimento(db, atendimento_id=atendimento_id)
    if db_atendimento is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    return db_atendimento