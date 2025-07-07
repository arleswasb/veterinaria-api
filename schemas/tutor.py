from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema base com os campos comuns
class TutorBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None

# Schema para criação (recebido via API)
class TutorCreate(TutorBase):
    pass

# Schema para atualização (recebido via API)
class TutorUpdate(TutorBase):
    pass

# Schema para leitura (retornado pela API)
class Tutor(TutorBase):
    id: int

    class Config:
        from_attributes = True