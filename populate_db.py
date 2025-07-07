#!/usr/bin/env python3
"""
Script para INICIALIZAR e POPULAR o banco de dados com dados de exemplo.
- Cria todas as tabelas (se não existirem).
- Popula o banco com dados de exemplo para demonstração.
"""

import datetime
import logging
from sqlalchemy.orm import sessionmaker
from database import engine, Base  # Importar Base para criar tabelas
from models.models import Usuario, Clinica, Veterinario, Tutor, Pet, Atendimento
from services.auth import get_password_hash

# Configurar logging para uma saída mais clara
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Criar uma fábrica de sessões que será usada para criar sessões individuais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Cria todas as tabelas no banco de dados."""
    try:
        logger.info("🔨 Criando todas as tabelas (se não existirem)...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        raise

def populate_db():
    """Popula o banco de dados com dados de exemplo."""
    db = SessionLocal()
    try:
        logger.info("🌱 Populando o banco de dados com dados de exemplo...")

        # Verificar se já existem dados para não duplicar
        if db.query(Usuario).first():
            logger.warning("⚠️  Dados de usuário já existem. Pulando a população para evitar duplicatas.")
            return

        # Criar usuários
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
        db.add_all([admin_user, user_demo])
        db.commit()
        logger.info("   - Usuários criados: admin (senha: admin123), demo (senha: demo123)")

        # Criar clínicas
        clinica1 = Clinica(nome="Clínica VetLife", cidade="São Paulo", endereco="Rua das Flores, 123 - Centro")
        clinica2 = Clinica(nome="Animal Care Center", cidade="Rio de Janeiro", endereco="Av. Copacabana, 456 - Copacabana")
        db.add_all([clinica1, clinica2])
        db.commit()

        # Criar veterinários
        vet1 = Veterinario(nome="Dr. João Silva", crmv="SP-12345", email="joao.silva@vetlife.com", especialidade="Clínica Geral", clinica_id=clinica1.id)
        vet2 = Veterinario(nome="Dra. Maria Santos", crmv="RJ-67890", email="maria.santos@animalcare.com", especialidade="Cirurgia", clinica_id=clinica2.id)
        db.add_all([vet1, vet2])
        db.commit()

        # Criar tutores
        tutor1 = Tutor(nome="Carlos Oliveira", telefone="(11) 99999-1234", email="carlos@email.com", endereco="Rua A, 100 - Vila Madalena")
        tutor2 = Tutor(nome="Ana Costa", telefone="(21) 88888-5678", email="ana@email.com", endereco="Rua B, 200 - Ipanema")
        db.add_all([tutor1, tutor2])
        db.commit()

        # Criar pets
        pet1 = Pet(nome="Rex", especie="Cão", raca="Golden Retriever", idade=3, tutor_id=tutor1.id)
        pet2 = Pet(nome="Mimi", especie="Gato", raca="Siamês", idade=2, tutor_id=tutor2.id)
        pet3 = Pet(nome="Buddy", especie="Cão", raca="Labrador", idade=5, tutor_id=tutor1.id)
        db.add_all([pet1, pet2, pet3])
        db.commit()

        # Criar atendimentos
        atendimento1 = Atendimento(descricao="Consulta de rotina e vacinação", data=datetime.datetime.now() - datetime.timedelta(days=7), pet_id=pet1.id, veterinario_id=vet1.id)
        atendimento2 = Atendimento(descricao="Cirurgia de castração", data=datetime.datetime.now() - datetime.timedelta(days=3), pet_id=pet2.id, veterinario_id=vet2.id)
        atendimento3 = Atendimento(descricao="Tratamento dermatológico", data=datetime.datetime.now() - datetime.timedelta(days=1), pet_id=pet3.id, veterinario_id=vet1.id)
        db.add_all([atendimento1, atendimento2, atendimento3])
        db.commit()

        logger.info("✅ Dados de exemplo criados com sucesso!")
        logger.info("📊 Resumo dos dados criados:")
        logger.info(f"   - {db.query(Clinica).count()} Clínicas")
        logger.info(f"   - {db.query(Veterinario).count()} Veterinários")
        logger.info(f"   - {db.query(Tutor).count()} Tutores")
        logger.info(f"   - {db.query(Pet).count()} Pets")
        logger.info(f"   - {db.query(Atendimento).count()} Atendimentos")

    except Exception as e:
        logger.error(f"❌ Erro ao popular o banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    populate_db()
