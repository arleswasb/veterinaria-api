from pydantic import BaseModel
from typing import Optional

# Schema base com os campos comuns
class ClinicaBase(BaseModel):
    nome: str
    cidade: Optional[str] = None
    endereco: str

# Schema para criação (recebido via API)
class ClinicaCreate(ClinicaBase):
    pass

# Schema para atualização (recebido via API)
class ClinicaUpdate(ClinicaBase):
    pass

# Schema para leitura (retornado pela API)
class Clinica(ClinicaBase):
    id: int

    class Config:
        from_attributes = True # Anteriormente orm_mode