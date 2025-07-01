from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from services import schemas
from repository import crud
from database import get_db
from services import veterinario_service # Importar o novo serviço
from services.auth import create_access_token
from services.dependencies import get_current_active_user
from config import settings

router = APIRouter(
    prefix="/api",
    tags=["veterinaria"]
)

# --- Endpoints para Autenticação ---

@router.post("/register", response_model=schemas.Usuario, status_code=201, summary="Registrar novo usuário")
def register_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário no sistema.
    - **username**: Nome de usuário único
    - **email**: Email único do usuário
    - **password**: Senha do usuário
    """
    # Verificar se username já existe
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username já está registrado"
        )
    
    # Verificar se email já existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email já está registrado"
        )
    
    return crud.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token, summary="Login para obter token")
async def login_for_access_token(login_form: schemas.LoginForm, db: Session = Depends(get_db)):
    """
    Autentica o usuário e retorna um token JWT.
    - **username**: Nome de usuário
    - **password**: Senha do usuário
    """
    user = crud.authenticate_user(db, login_form.username, login_form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.Usuario, summary="Obter dados do usuário atual")
async def read_users_me(current_user: schemas.Usuario = Depends(get_current_active_user)):
    """Retorna os dados do usuário autenticado."""
    return current_user

# --- Endpoints para Clínicas ---

@router.post("/clinicas", response_model=schemas.Clinica, status_code=201, summary="Cadastrar nova clínica")
def create_clinica_endpoint(
    clinica: schemas.ClinicaCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_active_user)
):
    """
    Cadastra uma nova clínica no sistema. Requer autenticação.
    - **nome**: Nome da clínica.
    - **cidade**: Cidade onde a clínica está localizada.
    - **endereco**: Endereço completo da clínica.
    """
    return crud.create_clinica(db=db, clinica=clinica)

@router.get("/clinicas", response_model=List[schemas.Clinica], summary="Listar todas as clínicas")
def read_clinicas_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as clínicas cadastradas."""
    return crud.get_clinicas(db, skip=skip, limit=limit)

@router.get("/clinicas/{id}", response_model=schemas.Clinica, summary="Listar clínica específica")
def read_clinica_endpoint(id: int, db: Session = Depends(get_db)):
    """Busca e retorna uma clínica específica pelo seu ID."""
    db_clinica = crud.get_clinica(db, clinica_id=id)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return db_clinica

@router.get("/clinicas/{id}/veterinarios", response_model=List[schemas.Veterinario], summary="Listar veterinários de uma clínica")
def read_veterinarios_from_clinica_endpoint(id: int, db: Session = Depends(get_db)):
    """Lista todos os veterinários associados a uma clínica específica."""
    db_clinica = crud.get_clinica(db, clinica_id=id)
    if db_clinica is None:
        raise HTTPException(status_code=404, detail="Clínica não encontrada")
    return crud.get_veterinarios_by_clinica(db, clinica_id=id)

# --- Endpoints para Veterinários ---

@router.post("/veterinarios", response_model=schemas.Veterinario, status_code=201, summary="Cadastrar novo veterinário")
def create_veterinario_endpoint(veterinario: schemas.VeterinarioCreate, db: Session = Depends(get_db)):
    """Cadastra um novo veterinário, aplicando regras de negócio."""
    return veterinario_service.create_new_veterinario(db=db, veterinario=veterinario)

@router.get("/veterinarios", response_model=List[schemas.Veterinario], summary="Listar todos os veterinários")
def read_veterinarios_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os veterinários cadastrados no sistema."""
    return crud.get_veterinarios(db, skip=skip, limit=limit)

@router.get("/veterinarios/{id}/atendimentos", response_model=List[schemas.Atendimento], summary="Listar atendimentos de um veterinário")
def read_atendimentos_from_veterinario_endpoint(id: int, db: Session = Depends(get_db)):
    """Retorna a lista de todos os atendimentos realizados por um veterinário específico."""
    db_veterinario = crud.get_veterinario(db, veterinario_id=id)
    if db_veterinario is None:
        raise HTTPException(status_code=404, detail="Veterinário não encontrado")
    return crud.get_atendimentos_by_veterinario(db, veterinario_id=id)

# --- Endpoints para Tutores ---

@router.post("/tutores", response_model=schemas.Tutor, status_code=201, summary="Cadastrar novo tutor")
def create_tutor_endpoint(tutor: schemas.TutorCreate, db: Session = Depends(get_db)):
    """Cadastra um novo tutor de pets no sistema."""
    return crud.create_tutor(db=db, tutor=tutor)

@router.get("/tutores/{id}/pets", response_model=List[schemas.Pet], summary="Listar pets de um tutor")
def read_pets_from_tutor_endpoint(id: int, db: Session = Depends(get_db)):
    """Retorna a lista de todos os pets pertencentes a um tutor específico."""
    db_tutor = crud.get_tutor(db, tutor_id=id)
    if db_tutor is None:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return crud.get_pets_by_tutor(db, tutor_id=id)

# --- Endpoints para Pets ---

@router.post("/pets", response_model=schemas.Pet, status_code=201, summary="Cadastrar novo pet")
def create_pet_endpoint(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    """Cadastra um novo pet e o associa a um tutor existente."""
    db_tutor = crud.get_tutor(db, tutor_id=pet.tutor_id)
    if not db_tutor:
        raise HTTPException(status_code=404, detail=f"Tutor com id {pet.tutor_id} não encontrado")
    return crud.create_pet_for_tutor(db=db, pet=pet)

@router.get("/pets", response_model=List[schemas.Pet], summary="Listar todos os pets")
def read_pets_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os pets cadastrados no sistema."""
    return crud.get_pets(db, skip=skip, limit=limit)

@router.get("/pets/{id}/atendimentos", response_model=List[schemas.Atendimento], summary="Listar atendimentos de um pet")
def read_atendimentos_from_pet_endpoint(id: int, db: Session = Depends(get_db)):
    """Retorna o histórico de atendimentos de um pet específico."""
    db_pet = crud.get_pet(db, pet_id=id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return crud.get_atendimentos_by_pet(db, pet_id=id)

# --- Endpoints para Atendimentos ---

@router.post("/atendimentos", response_model=schemas.Atendimento, status_code=201, summary="Criar novo atendimento")
def create_atendimento_endpoint(atendimento: schemas.AtendimentoCreate, db: Session = Depends(get_db)):
    """Registra um novo atendimento, vinculando um pet a um veterinário."""
    db_pet = crud.get_pet(db, pet_id=atendimento.pet_id)
    if not db_pet:
        raise HTTPException(status_code=404, detail=f"Pet com id {atendimento.pet_id} não encontrado")
    
    db_veterinario = crud.get_veterinario(db, veterinario_id=atendimento.veterinario_id)
    if not db_veterinario:
        raise HTTPException(status_code=404, detail=f"Veterinário com id {atendimento.veterinario_id} não encontrado")
        
    return crud.create_atendimento(db=db, atendimento=atendimento)

@router.get("/atendimentos", response_model=List[schemas.Atendimento], summary="Listar todos os atendimentos")
def read_atendimentos_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os atendimentos registrados no sistema."""
    return crud.get_atendimentos(db, skip=skip, limit=limit)