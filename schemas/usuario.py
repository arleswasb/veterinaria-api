from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema base com campos que podem ser expostos com segurança
class UsuarioBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

# Schema para criação (aceita password)
class UsuarioCreate(UsuarioBase):
    password: str

# Schema para atualização (campos opcionais)
class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Schema para leitura (retornado pela API)
# Não inclui o hashed_password por segurança
class Usuario(UsuarioBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True