"""
Rotas para gerenciamento de usuários.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import usuario as usuario_schema
from crud import usuario as usuario_crud
from services.auth import get_current_active_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    responses={404: {"description": "Usuário não encontrado"}},
    # Adiciona a dependência de autenticação a TODAS as rotas deste roteador
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/", response_model=usuario_schema.Usuario, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário."""
    # Verifica se o usuário já existe
    if usuario_crud.get_user_by_username(db, usuario.username):
        raise HTTPException(
            status_code=400,
            detail="Nome de usuário já cadastrado"
        )
    if usuario_crud.get_user_by_email(db, usuario.email):
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    return usuario_crud.create_user(db=db, user=usuario)

@router.get("/", response_model=List[usuario_schema.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os usuários."""
    usuarios = usuario_crud.get_users(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{user_id}", response_model=usuario_schema.Usuario)
def read_usuario(user_id: int, db: Session = Depends(get_db)):
    """Busca um usuário pelo ID."""
    db_usuario = usuario_crud.get_user(db, user_id=user_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.put("/{user_id}", response_model=usuario_schema.Usuario)
def update_usuario(user_id: int, usuario: usuario_schema.UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza um usuário existente."""
    db_usuario = usuario_crud.update_user(db, user_id=user_id, user=usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.delete("/{user_id}", response_model=usuario_schema.Usuario)
def delete_usuario(user_id: int, db: Session = Depends(get_db)):
    """Deleta um usuário."""
    db_usuario = usuario_crud.delete_user(db, user_id=user_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario
