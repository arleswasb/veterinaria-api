"""
Schemas para validação de dados de Veterinário.
"""
from pydantic import BaseModel
from typing import Optional


class VeterinarioBase(BaseModel):
    """Schema base para Veterinário."""
    nome: str
    crmv: str
    email: Optional[str] = None
    especialidade: Optional[str] = None
    clinica_id: int


class VeterinarioCreate(VeterinarioBase):
    """Schema para criação de Veterinário."""
    pass


class VeterinarioUpdate(BaseModel):
    """Schema para atualização de Veterinário."""
    nome: Optional[str] = None
    crmv: Optional[str] = None
    email: Optional[str] = None
    especialidade: Optional[str] = None
    clinica_id: Optional[int] = None


class Veterinario(VeterinarioBase):
    """Schema para resposta de Veterinário."""
    id: int

    class Config:
        from_attributes = True
