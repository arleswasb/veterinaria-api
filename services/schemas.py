from pydantic import BaseModel
from typing import List, Optional
import datetime

# Schemas para Pet
class PetBase(BaseModel):
    nome: str
    especie: str
    raca: Optional[str] = None
    idade: Optional[int] = None

class PetCreate(PetBase):
    tutor_id: int

class Pet(PetBase):
    id: int
    tutor_id: int

    class Config:
        from_attributes = True

# Schemas para Tutor
class TutorBase(BaseModel):
    nome: str
    telefone: str
    email: Optional[str] = None
    endereco: Optional[str] = None

class TutorCreate(TutorBase):
    pass

class Tutor(TutorBase):
    id: int
    pets: List[Pet] = []

    class Config:
        from_attributes = True

# Schemas para Atendimento
class AtendimentoBase(BaseModel):
    descricao: str

class AtendimentoCreate(AtendimentoBase):
    pet_id: int
    veterinario_id: int

class Atendimento(AtendimentoBase):
    id: int
    data: datetime.datetime
    pet_id: int
    veterinario_id: int

    class Config:
        from_attributes = True

# Schemas para Veterinário
class VeterinarioBase(BaseModel):
    nome: str
    crmv: str
    email: str
    especialidade: str

class VeterinarioCreate(VeterinarioBase):
    clinica_id: int

class Veterinario(VeterinarioBase):
    id: int
    clinica_id: int
    
    class Config:
        from_attributes = True

# Schemas para Clínica
class ClinicaBase(BaseModel):
    nome: str
    cidade: str
    endereco: Optional[str] = None

class ClinicaCreate(ClinicaBase):
    pass

class Clinica(ClinicaBase):
    id: int
    veterinarios: List[Veterinario] = []

    class Config:
        from_attributes = True