#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
para demonstração da API veterinária.
"""

from sqlalchemy.orm import sessionmaker
from database import engine
from models.models import Usuario, Clinica, Veterinario, Tutor, Pet, Atendimento
from services.auth import get_password_hash
import datetime

# Criar uma sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_sample_data():
    """Cria dados de exemplo no banco de dados."""
    
    print("🌱 Criando dados de exemplo...")
    
    try:
        # Verificar se já existem dados
        if db.query(Usuario).first():
            print("⚠️  Dados já existem no banco. Pulando criação de exemplos.")
            return
        
        # Criar usuário administrador
        admin_user = Usuario(
            username="admin",
            email="admin@veterinaria.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        
        user_demo = Usuario(
            username="demo",
            email="demo@veterinaria.com",
            hashed_password=get_password_hash("demo123"),
            is_active=True
        )
        
        db.add(admin_user)
        db.add(user_demo)
        db.commit()
        
        print("✅ Usuários criados:")
        print("   - admin (senha: admin123)")
        print("   - demo (senha: demo123)")
        
        # Criar clínicas
        clinica1 = Clinica(
            nome="Clínica VetLife",
            cidade="São Paulo",
            endereco="Rua das Flores, 123 - Centro"
        )
        
        clinica2 = Clinica(
            nome="Animal Care Center",
            cidade="Rio de Janeiro", 
            endereco="Av. Copacabana, 456 - Copacabana"
        )
        
        db.add(clinica1)
        db.add(clinica2)
        db.commit()
        
        # Criar veterinários
        vet1 = Veterinario(
            nome="Dr. João Silva",
            crmv="SP-12345",
            email="joao.silva@vetlife.com",
            especialidade="Clínica Geral",
            clinica_id=clinica1.id
        )
        
        vet2 = Veterinario(
            nome="Dra. Maria Santos",
            crmv="RJ-67890",
            email="maria.santos@animalcare.com",
            especialidade="Cirurgia",
            clinica_id=clinica2.id
        )
        
        db.add(vet1)
        db.add(vet2)
        db.commit()
        
        # Criar tutores
        tutor1 = Tutor(
            nome="Carlos Oliveira",
            telefone="(11) 99999-1234",
            email="carlos@email.com",
            endereco="Rua A, 100 - Vila Madalena"
        )
        
        tutor2 = Tutor(
            nome="Ana Costa",
            telefone="(21) 88888-5678", 
            email="ana@email.com",
            endereco="Rua B, 200 - Ipanema"
        )
        
        db.add(tutor1)
        db.add(tutor2)
        db.commit()
        
        # Criar pets
        pet1 = Pet(
            nome="Rex",
            especie="Cão",
            raca="Golden Retriever",
            idade=3,
            tutor_id=tutor1.id
        )
        
        pet2 = Pet(
            nome="Mimi",
            especie="Gato",
            raca="Siamês",
            idade=2,
            tutor_id=tutor2.id
        )
        
        pet3 = Pet(
            nome="Buddy",
            especie="Cão", 
            raca="Labrador",
            idade=5,
            tutor_id=tutor1.id
        )
        
        db.add(pet1)
        db.add(pet2)
        db.add(pet3)
        db.commit()
        
        # Criar atendimentos
        atendimento1 = Atendimento(
            descricao="Consulta de rotina e vacinação",
            data=datetime.datetime.now() - datetime.timedelta(days=7),
            pet_id=pet1.id,
            veterinario_id=vet1.id
        )
        
        atendimento2 = Atendimento(
            descricao="Cirurgia de castração",
            data=datetime.datetime.now() - datetime.timedelta(days=3),
            pet_id=pet2.id,
            veterinario_id=vet2.id
        )
        
        atendimento3 = Atendimento(
            descricao="Tratamento dermatológico",
            data=datetime.datetime.now() - datetime.timedelta(days=1),
            pet_id=pet3.id,
            veterinario_id=vet1.id
        )
        
        db.add(atendimento1)
        db.add(atendimento2) 
        db.add(atendimento3)
        db.commit()
        
        print("✅ Dados de exemplo criados com sucesso!")
        print("📊 Resumo dos dados criados:")
        print(f"   - {db.query(Clinica).count()} Clínicas")
        print(f"   - {db.query(Veterinario).count()} Veterinários")
        print(f"   - {db.query(Tutor).count()} Tutores")
        print(f"   - {db.query(Pet).count()} Pets")
        print(f"   - {db.query(Atendimento).count()} Atendimentos")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
