from sqlalchemy.orm import Session
from models import models
from services import schemas
from services.auth import get_password_hash

# --- CRUD para Usuario ---

def get_user_by_username(db: Session, username: str):
    """Busca um usuário pelo username."""
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Busca um usuário pelo email."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_user(db: Session, user: schemas.UsuarioCreate):
    """Cria um novo usuário com senha hasheada."""
    hashed_password = get_password_hash(user.password)
    db_user = models.Usuario(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Autentica um usuário verificando username e senha."""
    from services.auth import verify_password
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# --- CRUD para Clinica ---

def get_clinica(db: Session, clinica_id: int):
    """Busca uma única clínica pelo ID."""
    return db.query(models.Clinica).filter(models.Clinica.id == clinica_id).first()

def get_clinicas(db: Session, skip: int = 0, limit: int = 100):
    """Busca todas as clínicas com paginação."""
    return db.query(models.Clinica).offset(skip).limit(limit).all()

def create_clinica(db: Session, clinica: schemas.ClinicaCreate):
    """Cria uma nova clínica."""
    db_clinica = models.Clinica(nome=clinica.nome, cidade=clinica.cidade, endereco=clinica.endereco)
    db.add(db_clinica)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

# --- CRUD para Veterinario ---

def get_veterinario(db: Session, veterinario_id: int):
    """Busca um veterinário pelo ID."""
    return db.query(models.Veterinario).filter(models.Veterinario.id == veterinario_id).first()

def get_veterinarios(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os veterinários."""
    return db.query(models.Veterinario).offset(skip).limit(limit).all()

def get_veterinarios_by_clinica(db: Session, clinica_id: int):
    """Busca todos os veterinários de uma clínica específica."""
    return db.query(models.Veterinario).filter(models.Veterinario.clinica_id == clinica_id).all()

def create_veterinario(db: Session, veterinario: schemas.VeterinarioCreate):
    """Cria um novo veterinário associado a uma clínica."""
    db_veterinario = models.Veterinario(**veterinario.dict())
    db.add(db_veterinario)
    db.commit()
    db.refresh(db_veterinario)
    return db_veterinario

# --- CRUD para Tutor ---

def get_tutor(db: Session, tutor_id: int):
    """Busca um tutor pelo ID."""
    return db.query(models.Tutor).filter(models.Tutor.id == tutor_id).first()

def get_tutores(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os tutores."""
    return db.query(models.Tutor).offset(skip).limit(limit).all()

def create_tutor(db: Session, tutor: schemas.TutorCreate):
    """Cria um novo tutor."""
    db_tutor = models.Tutor(nome=tutor.nome, telefone=tutor.telefone, email=tutor.email)
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

# --- CRUD para Pet ---

def get_pet(db: Session, pet_id: int):
    """Busca um pet pelo ID."""
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def get_pets(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os pets."""
    return db.query(models.Pet).offset(skip).limit(limit).all()

def get_pets_by_tutor(db: Session, tutor_id: int):
    """Busca todos os pets de um tutor específico."""
    return db.query(models.Pet).filter(models.Pet.tutor_id == tutor_id).all()

def create_pet_for_tutor(db: Session, pet: schemas.PetCreate):
    """Cria um novo pet para um tutor."""
    db_pet = models.Pet(**pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

# --- CRUD para Atendimento ---

def get_atendimentos(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os atendimentos."""
    return db.query(models.Atendimento).offset(skip).limit(limit).all()

def create_atendimento(db: Session, atendimento: schemas.AtendimentoCreate):
    """Cria um novo atendimento."""
    db_atendimento = models.Atendimento(**atendimento.dict())
    db.add(db_atendimento)
    db.commit()
    db.refresh(db_atendimento)
    return db_atendimento

def get_atendimentos_by_pet(db: Session, pet_id: int):
    """Busca todos os atendimentos de um pet específico."""
    return db.query(models.Atendimento).filter(models.Atendimento.pet_id == pet_id).all()

def get_atendimentos_by_veterinario(db: Session, veterinario_id: int):
    """Busca todos os atendimentos de um veterinário específico."""
    return db.query(models.Atendimento).filter(models.Atendimento.veterinario_id == veterinario_id).all()