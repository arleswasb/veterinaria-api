from pydantic import BaseModel
from typing import Optional

# Schema base com os campos comuns
class PetBase(BaseModel):
    nome: str
    especie: str
    raca: Optional[str] = None
    idade: Optional[int] = None

# Schema para criação (recebido via API)
# Um pet deve estar associado a um tutor no momento da criação
class PetCreate(PetBase):
    tutor_id: int

# Schema para atualização (recebido via API)
# Não permitimos a alteração do tutor de um pet via este endpoint
class PetUpdate(PetBase):
    pass

# Schema para leitura (retornado pela API)
# Inclui o ID do pet e do seu tutor
class Pet(PetBase):
    id: int
    tutor_id: int

    class Config:
        from_attributes = True