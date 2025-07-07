#!/usr/bin/env python3
"""
Script para validar se a aplicação pode ser inicializada corretamente.
"""

import sys
import traceback
from config import settings

def validate_configuration():
    """Valida as configurações da aplicação."""
    print("🔧 Validando configurações...")
    
    # Verificar configurações básicas
    print(f"   App Name: {settings.app_name}")
    print(f"   Version: {settings.app_version}")
    print(f"   Environment: {settings.environment}")
    print(f"   Debug: {settings.debug}")
    print(f"   Database URL: {settings.effective_database_url}")
    
    return True

def validate_database_connection():
    """Testa a conexão com o banco de dados."""
    print("🗄️ Testando conexão com banco de dados...")
    
    try:
        from database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("   ✅ Conexão com banco estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"   ❌ Erro na conexão: {e}")
        return False

def validate_models():
    """Valida se os modelos podem ser importados."""
    print("📋 Validando modelos...")
    
    try:
        from models import models
        print("   ✅ Modelos importados com sucesso!")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao importar modelos: {e}")
        return False

def validate_routes():
    """Valida se as rotas podem ser importadas."""
    print("🛣️ Validando rotas...")
    
    try:
        from api import routes
        print("   ✅ Rotas importadas com sucesso!")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao importar rotas: {e}")
        return False

def validate_main_app():
    """Testa se a aplicação principal pode ser inicializada."""
    print("🚀 Validando aplicação principal...")
    
    try:
        # Importar sem executar
        import main
        print("   ✅ Aplicação pode ser inicializada!")
        return True
    except Exception as e:
        print(f"   ❌ Erro na aplicação: {e}")
        traceback.print_exc()
        return False

def main():
    """Executa todas as validações."""
    print("🔍 VALIDAÇÃO DE INICIALIZAÇÃO DA API VETERINÁRIA")
    print("=" * 50)
    
    validations = [
        validate_configuration,
        validate_models,
        validate_routes,
        validate_database_connection,
        validate_main_app
    ]
    
    results = []
    for validation in validations:
        try:
            result = validation()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")
            results.append(False)
        print()
    
    # Resumo
    print("📊 RESUMO DAS VALIDAÇÕES")
    print("=" * 30)
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print("🎉 Todas as validações passaram! A aplicação está pronta.")
        return 0
    else:
        print(f"⚠️ {success_count}/{total_count} validações passaram.")
        print("Verifique os erros acima antes de executar a aplicação.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
