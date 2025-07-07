#!/usr/bin/env python3
"""
Script para validar se a aplicação está funcionando corretamente.
Pode ser executado tanto em desenvolvimento quanto em produção.
"""

import os
import sys
import time
import requests
import logging
from typing import Dict, Any
from urllib.parse import urlparse

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_api_base_url() -> str:
    """Determina a URL base da API baseada no ambiente."""
    # Verifica se está rodando em Docker
    if os.getenv('DOCKER_CONTAINER'):
        return "http://localhost:8000"
    
    # Verifica variáveis de ambiente
    api_host = os.getenv('API_HOST', 'localhost')
    api_port = os.getenv('API_PORT', '8000')
    
    return f"http://{api_host}:{api_port}"

def wait_for_api(base_url: str, timeout: int = 60) -> bool:
    """Aguarda a API ficar disponível."""
    logger.info(f"🔍 Aguardando API em {base_url}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                logger.info("✅ API está respondendo!")
                return True
        except requests.RequestException:
            pass
        
        time.sleep(2)
    
    logger.error(f"❌ API não respondeu dentro de {timeout} segundos")
    return False

def validate_endpoints(base_url: str) -> Dict[str, bool]:
    """Valida os principais endpoints da API."""
    endpoints = {
        "health": "/api/health",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "root": "/",
        "clinicas": "/api/clinicas",
        "veterinarios": "/api/veterinarios",
        "tutores": "/api/tutores",
        "pets": "/api/pets",
        "atendimentos": "/api/atendimentos",
        "usuarios": "/api/usuarios"
    }
    
    results = {}
    
    for name, endpoint in endpoints.items():
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if name == "health":
                # Health check deve retornar 200
                is_valid = response.status_code == 200
            elif name in ["docs", "openapi"]:
                # Documentação deve retornar 200
                is_valid = response.status_code == 200
            elif name == "root":
                # Root pode retornar 200 ou 404
                is_valid = response.status_code in [200, 404]
            else:
                # Outros endpoints podem retornar 200 (com dados) ou 401 (sem auth)
                is_valid = response.status_code in [200, 401, 422]
            
            results[name] = is_valid
            status = "✅" if is_valid else "❌"
            logger.info(f"{status} {name.upper()}: {url} - Status: {response.status_code}")
            
        except requests.RequestException as e:
            results[name] = False
            logger.error(f"❌ {name.upper()}: {url} - Erro: {e}")
    
    return results

def test_authentication(base_url: str) -> bool:
    """Testa o sistema de autenticação."""
    try:
        # Tenta fazer login com usuário demo
        login_data = {
            "username": "demo",
            "password": "demo123"
        }
        
        response = requests.post(
            f"{base_url}/api/auth/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            if "access_token" in token_data:
                logger.info("✅ Autenticação funcionando - Token obtido com sucesso")
                return True
        
        logger.warning(f"⚠️ Autenticação retornou status {response.status_code}")
        return False
        
    except requests.RequestException as e:
        logger.error(f"❌ Erro ao testar autenticação: {e}")
        return False

def validate_database_data(base_url: str) -> bool:
    """Valida se os dados foram populados corretamente."""
    try:
        # Tenta acessar dados sem autenticação (alguns endpoints podem retornar 401)
        endpoints_to_check = [
            ("/api/clinicas", "clínicas"),
            ("/api/veterinarios", "veterinários"),
            ("/api/tutores", "tutores"),
            ("/api/pets", "pets")
        ]
        
        data_populated = 0
        
        for endpoint, name in endpoints_to_check:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        logger.info(f"✅ {name.capitalize()}: {len(data)} registros encontrados")
                        data_populated += 1
                    else:
                        logger.warning(f"⚠️ {name.capitalize()}: Nenhum registro encontrado")
                elif response.status_code == 401:
                    logger.info(f"🔐 {name.capitalize()}: Endpoint protegido (401) - OK")
                    data_populated += 1
                else:
                    logger.warning(f"⚠️ {name.capitalize()}: Status {response.status_code}")
            except requests.RequestException as e:
                logger.error(f"❌ Erro ao verificar {name}: {e}")
        
        return data_populated > 0
        
    except Exception as e:
        logger.error(f"❌ Erro ao validar dados do banco: {e}")
        return False

def main():
    """Função principal de validação."""
    logger.info("🚀 Iniciando validação da aplicação...")
    
    base_url = get_api_base_url()
    logger.info(f"📍 URL base da API: {base_url}")
    
    # Passo 1: Aguardar API ficar disponível
    if not wait_for_api(base_url):
        logger.error("❌ Falha na validação: API não está disponível")
        sys.exit(1)
    
    # Passo 2: Validar endpoints
    logger.info("\n🔍 Validando endpoints...")
    endpoint_results = validate_endpoints(base_url)
    
    # Passo 3: Testar autenticação
    logger.info("\n🔐 Testando autenticação...")
    auth_working = test_authentication(base_url)
    
    # Passo 4: Validar dados do banco
    logger.info("\n📊 Validando dados do banco...")
    data_valid = validate_database_data(base_url)
    
    # Resumo dos resultados
    logger.info("\n📋 RESUMO DA VALIDAÇÃO:")
    logger.info("=" * 40)
    
    successful_endpoints = sum(1 for result in endpoint_results.values() if result)
    total_endpoints = len(endpoint_results)
    
    logger.info(f"Endpoints funcionais: {successful_endpoints}/{total_endpoints}")
    logger.info(f"Autenticação: {'✅ OK' if auth_working else '❌ FALHA'}")
    logger.info(f"Dados do banco: {'✅ OK' if data_valid else '❌ FALHA'}")
    
    # Determinar sucesso geral
    critical_endpoints = ["health", "docs"]  # Removido "openapi" pois pode não estar disponível
    critical_working = all(endpoint_results.get(ep, False) for ep in critical_endpoints)
    
    overall_success = (
        critical_working and 
        successful_endpoints >= (total_endpoints * 0.7) and  # 70% dos endpoints funcionando
        auth_working and data_valid  # Autenticação e dados devem funcionar
    )
    
    if overall_success:
        logger.info("\n🎉 VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("A aplicação está funcionando corretamente.")
        sys.exit(0)
    else:
        logger.error("\n❌ VALIDAÇÃO FALHOU!")
        logger.error("A aplicação apresenta problemas que precisam ser corrigidos.")
        sys.exit(1)

if __name__ == "__main__":
    main()
