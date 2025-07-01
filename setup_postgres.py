#!/usr/bin/env python3
"""
Script para configurar e testar conexão com PostgreSQL
"""

import subprocess
import sys
import os
from sqlalchemy import create_engine, text
from config import settings

def check_postgresql_installation():
    """Verifica se o PostgreSQL está instalado."""
    try:
        result = subprocess.run(['psql', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PostgreSQL não está instalado ou não está no PATH")
        return False

def install_postgresql_windows():
    """Instruções para instalar PostgreSQL no Windows."""
    print("\n🔧 Como instalar PostgreSQL no Windows:")
    print("1. Baixe o instalador em: https://www.postgresql.org/download/windows/")
    print("2. Execute o instalador e siga as instruções")
    print("3. Defina uma senha para o usuário 'postgres'")
    print("4. Mantenha a porta padrão 5432")
    print("5. Após a instalação, adicione o PostgreSQL ao PATH:")
    print("   - Vá em Variáveis de Ambiente")
    print("   - Adicione C:\\Program Files\\PostgreSQL\\15\\bin ao PATH")
    print("\nOu instale via Chocolatey:")
    print("choco install postgresql")
    print("\nOu via Scoop:")
    print("scoop install postgresql")

def create_database():
    """Cria o banco de dados veterinaria_db."""
    try:
        # Conecta ao PostgreSQL como superusuário para criar o banco
        admin_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/postgres"
        engine = create_engine(admin_url)
        
        with engine.connect() as conn:
            # Não podemos usar transação para CREATE DATABASE
            conn.execute(text("COMMIT"))
            try:
                conn.execute(text(f"CREATE DATABASE {settings.postgres_db}"))
                print(f"✅ Banco de dados '{settings.postgres_db}' criado com sucesso!")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"ℹ️  Banco de dados '{settings.postgres_db}' já existe")
                else:
                    raise e
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        print("\n🔧 Possíveis soluções:")
        print("1. Verifique se o PostgreSQL está rodando")
        print("2. Verifique as credenciais no arquivo .env")
        print("3. Certifique-se de que o usuário tem permissões")
        return False

def test_connection():
    """Testa a conexão com o banco de dados."""
    try:
        engine = create_engine(settings.postgres_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conexão PostgreSQL bem-sucedida!")
            print(f"📋 Versão: {version[:50]}...")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def setup_postgresql():
    """Processo completo de configuração do PostgreSQL."""
    print("🐘 Configuração PostgreSQL para API Veterinária\n")
    
    # 1. Verificar instalação
    if not check_postgresql_installation():
        install_postgresql_windows()
        print("\n⚠️  Instale o PostgreSQL e execute este script novamente.")
        return False
    
    # 2. Verificar configurações
    print(f"\n📋 Configurações atuais:")
    print(f"   Host: {settings.postgres_host}")
    print(f"   Port: {settings.postgres_port}")
    print(f"   User: {settings.postgres_user}")
    print(f"   Database: {settings.postgres_db}")
    
    # 3. Criar banco de dados
    print(f"\n🗄️  Criando banco de dados...")
    if not create_database():
        return False
    
    # 4. Testar conexão
    print(f"\n🔌 Testando conexão...")
    if not test_connection():
        return False
    
    print(f"\n✅ PostgreSQL configurado com sucesso!")
    print(f"\n📝 Para usar PostgreSQL, atualize seu .env:")
    print(f"DATABASE_URL={settings.postgres_url}")
    print(f"ENVIRONMENT=production")
    
    return True

def show_status():
    """Mostra o status atual da configuração."""
    print("📊 Status atual da configuração:\n")
    print(f"Environment: {settings.environment}")
    print(f"Database URL: {settings.database_url}")
    print(f"Effective URL: {settings.effective_database_url}")
    
    if settings.effective_database_url.startswith("sqlite"):
        print("🔧 Usando SQLite (desenvolvimento)")
    else:
        print("🐘 Usando PostgreSQL (produção)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_status()
    else:
        setup_postgresql()
