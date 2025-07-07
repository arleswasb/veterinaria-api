from pydantic import BaseModel
from typing import Optional
import datetime

# Schema base com os campos comuns
class AtendimentoBase(BaseModel):
    descricao: str

# Schema para criação (recebido via API)
class AtendimentoCreate(AtendimentoBase):
    pet_id: int
    veterinario_id: int

# Schema para atualização (recebido via API)
# Permite atualizar apenas a descrição
class AtendimentoUpdate(BaseModel):
    descricao: Optional[str] = None

# Schema para leitura (retornado pela API)
class Atendimento(AtendimentoBase):
    id: int
    data: datetime.datetime
    pet_id: int
    veterinario_id: int

    class Config:
        from_attributes = True