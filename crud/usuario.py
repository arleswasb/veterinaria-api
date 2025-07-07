from sqlalchemy.orm import Session
from models import models
from schemas import usuario as usuario_schema


def get_user_by_username(db: Session, username: str):
    """Busca um usuário pelo nome de usuário."""
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Busca um usuário pelo email."""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def create_user(db: Session, user: usuario_schema.UsuarioCreate):
    """Cria um novo usuário com senha hasheada."""
    from services.auth import get_password_hash
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


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os usuários com paginação."""
    return db.query(models.Usuario).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    """Busca um usuário pelo ID."""
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()


def update_user(db: Session, user_id: int, user: usuario_schema.UsuarioUpdate):
    """Atualiza um usuário existente."""
    from services.auth import get_password_hash
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            if key == "password":
                setattr(db_user, "hashed_password", get_password_hash(value))
            else:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Deleta um usuário."""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user