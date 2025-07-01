#!/usr/bin/env python3
"""
Script para inicializar o banco de dados da aplicação veterinária.
Cria todas as tabelas necessárias baseadas nos modelos SQLAlchemy.
Funciona com SQLite (desenvolvimento) e PostgreSQL (produção).
"""

from database import engine, Base, DATABASE_URL
from models.models import Clinica, Veterinario, Tutor, Pet, Atendimento
from config import settings

def init_database():
    """Inicializa o banco de dados criando todas as tabelas."""
    print("🗄️  Inicializando banco de dados...")
    print(f"📋 Tipo: {'PostgreSQL' if DATABASE_URL.startswith('postgresql') else 'SQLite'}")
    print(f"📍 URL: {DATABASE_URL}")
    
    try:
        print("\n🔨 Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tabelas criadas com sucesso!")
        print("📋 Tabelas criadas:")
        print("   - clinicas (Clínicas)")
        print("   - veterinarios (Veterinários)") 
        print("   - tutores (Tutores)")
        print("   - pets (Pets)")
        print("   - atendimentos (Atendimentos)")
        
        # Verificar se as tabelas foram criadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n📊 {len(tables)} tabelas encontradas no banco:")
        for table in tables:
            print(f"   ✓ {table}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        
        # Dicas de solução baseadas no erro
        if "connection" in str(e).lower():
            print("\n🔧 Dicas para resolver problemas de conexão:")
            if DATABASE_URL.startswith('postgresql'):
                print("1. Verifique se o PostgreSQL está rodando")
                print("2. Confirme as credenciais no arquivo .env")
                print("3. Execute: python setup_postgres.py")
            else:
                print("1. Verifique permissões na pasta do projeto")
                print("2. Certifique-se de que não há arquivos bloqueados")
        
        return False

if __name__ == "__main__":
    init_database()