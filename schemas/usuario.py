from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema base com campos que podem ser expostos com segurança
class UsuarioBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

# Schema para leitura (retornado pela API)
# Não inclui o hashed_password por segurança
class Usuario(UsuarioBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True