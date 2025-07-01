import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Clinica(Base):
    __tablename__ = 'clinicas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    endereco = Column(String)
    cidade = Column(String, nullable=False)

    # Relacionamento: Uma clínica tem vários veterinários
    veterinarios = relationship("Veterinario", back_populates="clinica")

class Veterinario(Base):
    __tablename__ = 'veterinarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    crmv = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True)
    especialidade = Column(String)

    # Relacionamento: Um veterinário pertence a uma clínica
    clinica_id = Column(Integer, ForeignKey('clinicas.id'))
    clinica = relationship("Clinica", back_populates="veterinarios")

    # Relacionamento: Um veterinário realiza vários atendimentos
    atendimentos = relationship("Atendimento", back_populates="veterinario")

class Tutor(Base):
    __tablename__ = 'tutores'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    endereco = Column(String)

    # Relacionamento: Um tutor tem vários pets
    pets = relationship("Pet", back_populates="tutor")

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especie = Column(String)
    raca = Column(String)
    idade = Column(Integer)

    # Relacionamento: Um pet pertence a um tutor
    tutor_id = Column(Integer, ForeignKey('tutores.id'))
    tutor = relationship("Tutor", back_populates="pets")

    # Relacionamento: Um pet pode ter vários atendimentos
    atendimentos = relationship("Atendimento", back_populates="pet")

class Atendimento(Base):
    __tablename__ = 'atendimentos'
    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.datetime.utcnow)
    descricao = Column(String, nullable=False)

    # Relacionamento: Um atendimento é de um pet
    pet_id = Column(Integer, ForeignKey('pets.id'))
    pet = relationship("Pet", back_populates="atendimentos")

    # Relacionamento: Um atendimento é realizado por um veterinário
    veterinario_id = Column(Integer, ForeignKey('veterinarios.id'))
    veterinario = relationship("Veterinario", back_populates="atendimentos")