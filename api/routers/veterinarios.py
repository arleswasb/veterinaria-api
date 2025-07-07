from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import veterinario as veterinario_schema
from crud import veterinario as veterinario_crud
from services.auth import get_current_active_user
from schemas import usuario as usuario_schema

router = APIRouter(
    prefix="/veterinarios",
    tags=["Veterinários"],
    responses={404: {"description": "Veterinário não encontrado"}},
    # Adiciona a dependência de autenticação a TODAS as rotas deste roteador
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=veterinario_schema.Veterinario, status_code=status.HTTP_201_CREATED)
def create_veterinario(veterinario: veterinario_schema.VeterinarioCreate, db: Session = Depends(get_db)):
    """Cria um novo veterinário."""
    return veterinario_crud.create_veterinario(db=db, veterinario=veterinario)

@router.get("/", response_model=List[veterinario_schema.Veterinario])
def read_veterinarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os veterinários."""
    veterinarios = veterinario_crud.get_veterinarios(db, skip=skip, limit=limit)
    return veterinarios

@router.get("/{veterinario_id}", response_model=veterinario_schema.Veterinario)
def read_veterinario(veterinario_id: int, db: Session = Depends(get_db)):
    """Busca um veterinário pelo ID."""
    db_veterinario = veterinario_crud.get_veterinario(db, veterinario_id=veterinario_id)
    if db_veterinario is None:
        raise HTTPException(status_code=404, detail="Veterinário não encontrado")
    return db_veterinario

@router.put("/{veterinario_id}", response_model=veterinario_schema.Veterinario)
def update_veterinario(veterinario_id: int, veterinario: veterinario_schema.VeterinarioCreate, db: Session = Depends(get_db)):
    """Atualiza um veterinário existente."""
    db_veterinario = veterinario_crud.update_veterinario(db, veterinario_id=veterinario_id, veterinario=veterinario)
    if db_veterinario is None:
        raise HTTPException(status_code=404, detail="Veterinário não encontrado")
    return db_veterinario

@router.delete("/{veterinario_id}", response_model=veterinario_schema.Veterinario)
def delete_veterinario(veterinario_id: int, db: Session = Depends(get_db)):
    """Deleta um veterinário."""
    db_veterinario = veterinario_crud.delete_veterinario(db, veterinario_id=veterinario_id)
    if db_veterinario is None:
        raise HTTPException(status_code=404, detail="Veterinário não encontrado")
    return db_veterinario