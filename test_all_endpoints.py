#!/usr/bin/env python3
"""
Script de simulação para testar todos os endpoints da API Veterinária.
Mostra resultados detalhados no terminal com cores e formatação.
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime
import sys

# Configurações
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

# Cores para terminal (ANSI)
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(title: str):
    """Imprime um cabeçalho formatado."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")

def print_section(title: str):
    """Imprime uma seção formatada."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 {title}{Colors.END}")
    print(f"{Colors.BLUE}{'-'*50}{Colors.END}")

def print_success(message: str):
    """Imprime mensagem de sucesso."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message: str):
    """Imprime mensagem de erro."""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message: str):
    """Imprime mensagem de aviso."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message: str):
    """Imprime mensagem informativa."""
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

def format_response(response: requests.Response) -> str:
    """Formata a resposta HTTP para exibição."""
    try:
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return response.text[:500] + "..." if len(response.text) > 500 else response.text
    except:
        return response.text[:200] + "..." if len(response.text) > 200 else response.text

def test_endpoint(method: str, url: str, description: str, data: Optional[Dict] = None, 
                 headers: Optional[Dict] = None, expected_status: int = 200) -> Dict[str, Any]:
    """Testa um endpoint e retorna informações sobre o resultado."""
    try:
        print(f"\n{Colors.BOLD}🚀 Testando: {description}{Colors.END}")
        print(f"   📍 {method.upper()} {url}")
        
        if data:
            print(f"   📤 Dados: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        start_time = time.time()
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=TIMEOUT)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=TIMEOUT)
        else:
            raise ValueError(f"Método HTTP não suportado: {method}")
        
        elapsed_time = time.time() - start_time
        
        # Analisa o resultado
        if response.status_code == expected_status:
            print_success(f"Status: {response.status_code} (Esperado: {expected_status}) - Tempo: {elapsed_time:.2f}s")
            result = "SUCCESS"
        elif response.status_code in [401, 403] and expected_status in [401, 403]:
            print_success(f"Status: {response.status_code} (Endpoint protegido como esperado) - Tempo: {elapsed_time:.2f}s")
            result = "PROTECTED"
        else:
            print_error(f"Status: {response.status_code} (Esperado: {expected_status}) - Tempo: {elapsed_time:.2f}s")
            result = "FAIL"
        
        # Mostra a resposta
        if response.status_code < 300:
            print(f"   📥 {Colors.GREEN}Resposta:{Colors.END}")
        elif response.status_code < 400:
            print(f"   📥 {Colors.YELLOW}Resposta:{Colors.END}")
        else:
            print(f"   📥 {Colors.RED}Resposta:{Colors.END}")
        
        formatted_response = format_response(response)
        for line in formatted_response.split('\n')[:10]:  # Mostra apenas as primeiras 10 linhas
            print(f"      {line}")
        
        if len(formatted_response.split('\n')) > 10:
            print(f"      {Colors.YELLOW}... (resposta truncada){Colors.END}")
        
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "expected_status": expected_status,
            "elapsed_time": elapsed_time,
            "result": result,
            "response_data": response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
        
    except requests.exceptions.Timeout:
        print_error(f"Timeout após {TIMEOUT}s")
        return {"url": url, "method": method, "result": "TIMEOUT", "error": "Timeout"}
    except requests.exceptions.ConnectionError:
        print_error("Erro de conexão - API não está rodando?")
        return {"url": url, "method": method, "result": "CONNECTION_ERROR", "error": "Connection failed"}
    except Exception as e:
        print_error(f"Erro inesperado: {str(e)}")
        return {"url": url, "method": method, "result": "ERROR", "error": str(e)}

def authenticate() -> Optional[str]:
    """Tenta fazer login e retorna o token de acesso."""
    print_section("🔐 AUTENTICAÇÃO")
    
    # Dados de teste (conforme o populate_db.py)
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        print_info("Tentando fazer login com usuário: admin")
        response = requests.post(
            f"{BASE_URL}/api/auth/token",
            data=login_data,  # OAuth2PasswordRequestForm usa form-data, não JSON
            headers=headers,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print_success(f"Login realizado com sucesso! Token obtido.")
            print(f"   🎫 Token: {token[:50]}...")
            return token
        else:
            print_error(f"Falha no login: {response.status_code}")
            print(f"   📥 Resposta: {format_response(response)}")
            return None
            
    except Exception as e:
        print_error(f"Erro durante autenticação: {str(e)}")
        return None

def test_endpoints_with_auth(token: str) -> Dict[str, Any]:
    """Testa endpoints que requerem autenticação."""
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    
    print_section("🔒 ENDPOINTS PROTEGIDOS")
    
    # Teste de listagem
    endpoints_to_test = [
        ("GET", f"{BASE_URL}/api/clinicas", "Listar Clínicas", None, 200),
        ("GET", f"{BASE_URL}/api/veterinarios", "Listar Veterinários", None, 200),
        ("GET", f"{BASE_URL}/api/tutores", "Listar Tutores", None, 200),
        ("GET", f"{BASE_URL}/api/pets", "Listar Pets", None, 200),
        ("GET", f"{BASE_URL}/api/atendimentos", "Listar Atendimentos", None, 200),
        ("GET", f"{BASE_URL}/api/usuarios", "Listar Usuários", None, 200),
    ]
    
    for method, url, description, data, expected_status in endpoints_to_test:
        result = test_endpoint(method, url, description, data, headers, expected_status)
        results.append(result)
    
    return results

def test_crud_operations(token: str) -> Dict[str, Any]:
    """Testa operações CRUD completas."""
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    
    print_section("🔧 OPERAÇÕES CRUD")
    
    # Teste de criação de clínica
    clinica_data = {
        "nome": "Clínica API Teste",
        "cidade": "São Paulo",
        "endereco": "Rua Teste da API, 123"
    }
    
    result = test_endpoint(
        "POST", 
        f"{BASE_URL}/api/clinicas", 
        "Criar Nova Clínica", 
        clinica_data, 
        headers, 
        201
    )
    results.append(result)
    
    # Se a criação foi bem-sucedida, tenta operações com o ID criado
    if result.get("result") == "SUCCESS" and result.get("response_data"):
        clinica_id = result["response_data"].get("id")
        if clinica_id:
            # Buscar clínica específica
            result = test_endpoint(
                "GET", 
                f"{BASE_URL}/api/clinicas/{clinica_id}", 
                f"Buscar Clínica ID {clinica_id}", 
                None, 
                headers, 
                200
            )
            results.append(result)
            
            # Atualizar clínica
            update_data = {
                "nome": "Clínica API Teste - Atualizada",
                "cidade": "Rio de Janeiro",
                "endereco": "Rua Teste Atualizada, 456"
            }
            
            result = test_endpoint(
                "PUT", 
                f"{BASE_URL}/api/clinicas/{clinica_id}", 
                f"Atualizar Clínica ID {clinica_id}", 
                update_data, 
                headers, 
                200
            )
            results.append(result)
    
    return results

def test_public_endpoints() -> Dict[str, Any]:
    """Testa endpoints públicos."""
    results = []
    
    print_section("🌐 ENDPOINTS PÚBLICOS")
    
    public_endpoints = [
        ("GET", f"{BASE_URL}/", "Página Inicial", None, 200),
        ("GET", f"{BASE_URL}/docs", "Documentação Swagger", None, 200),
        ("GET", f"{BASE_URL}/redoc", "Documentação ReDoc", None, 200),
        ("GET", f"{BASE_URL}/openapi.json", "Schema OpenAPI", None, 200),
        ("GET", f"{BASE_URL}/api/health", "Health Check", None, 200),
    ]
    
    for method, url, description, data, expected_status in public_endpoints:
        result = test_endpoint(method, url, description, data, None, expected_status)
        results.append(result)
    
    return results

def test_protected_without_auth() -> Dict[str, Any]:
    """Testa endpoints protegidos sem autenticação."""
    results = []
    
    print_section("🚫 ENDPOINTS PROTEGIDOS (SEM AUTH)")
    
    protected_endpoints = [
        ("GET", f"{BASE_URL}/api/clinicas", "Listar Clínicas (sem auth)", None, 401),
        ("GET", f"{BASE_URL}/api/veterinarios", "Listar Veterinários (sem auth)", None, 401),
        ("GET", f"{BASE_URL}/api/tutores", "Listar Tutores (sem auth)", None, 401),
        ("GET", f"{BASE_URL}/api/pets", "Listar Pets (sem auth)", None, 401),
        ("GET", f"{BASE_URL}/api/atendimentos", "Listar Atendimentos (sem auth)", None, 401),
        ("GET", f"{BASE_URL}/api/usuarios", "Listar Usuários (sem auth)", None, 401),
    ]
    
    for method, url, description, data, expected_status in protected_endpoints:
        result = test_endpoint(method, url, description, data, None, expected_status)
        results.append(result)
    
    return results

def print_summary(all_results: Dict[str, list]):
    """Imprime um resumo dos testes."""
    print_header("📊 RESUMO FINAL DOS TESTES")
    
    total_tests = 0
    successful_tests = 0
    protected_tests = 0
    failed_tests = 0
    
    for category, results in all_results.items():
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}📋 {category}{Colors.END}")
        
        category_success = 0
        category_protected = 0
        category_fail = 0
        
        for result in results:
            total_tests += 1
            status = result.get("result", "UNKNOWN")
            
            if status == "SUCCESS":
                successful_tests += 1
                category_success += 1
                print_success(f"{result.get('method', '?')} {result.get('url', '?')} - {result.get('status_code', '?')}")
            elif status == "PROTECTED":
                protected_tests += 1
                category_protected += 1
                print_success(f"{result.get('method', '?')} {result.get('url', '?')} - {result.get('status_code', '?')} (Protegido)")
            else:
                failed_tests += 1
                category_fail += 1
                print_error(f"{result.get('method', '?')} {result.get('url', '?')} - {status}")
        
        print(f"   📈 Sucessos: {category_success}, Protegidos: {category_protected}, Falhas: {category_fail}")
    
    # Estatísticas gerais
    print(f"\n{Colors.BOLD}{Colors.WHITE}📊 ESTATÍSTICAS GERAIS{Colors.END}")
    print(f"   🎯 Total de testes: {total_tests}")
    print(f"   ✅ Sucessos: {successful_tests}")
    print(f"   🔒 Protegidos (esperado): {protected_tests}")
    print(f"   ❌ Falhas: {failed_tests}")
    
    success_rate = ((successful_tests + protected_tests) / total_tests * 100) if total_tests > 0 else 0
    
    if success_rate >= 90:
        print(f"   🏆 {Colors.GREEN}Taxa de sucesso: {success_rate:.1f}% - EXCELENTE!{Colors.END}")
    elif success_rate >= 80:
        print(f"   🥈 {Colors.YELLOW}Taxa de sucesso: {success_rate:.1f}% - BOM{Colors.END}")
    else:
        print(f"   🚨 {Colors.RED}Taxa de sucesso: {success_rate:.1f}% - PRECISA MELHORAR{Colors.END}")

def main():
    """Função principal que executa todos os testes."""
    print_header("🏥 TESTE COMPLETO DA API VETERINÁRIA")
    print(f"{Colors.CYAN}⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.CYAN}🌐 URL Base: {BASE_URL}{Colors.END}")
    
    all_results = {}
    
    # 1. Testa endpoints públicos
    all_results["Endpoints Públicos"] = test_public_endpoints()
    
    # 2. Testa endpoints protegidos sem autenticação
    all_results["Proteção de Endpoints"] = test_protected_without_auth()
    
    # 3. Faz autenticação
    token = authenticate()
    
    if token:
        # 4. Testa endpoints com autenticação
        all_results["Endpoints Autenticados"] = test_endpoints_with_auth(token)
        
        # 5. Testa operações CRUD
        all_results["Operações CRUD"] = test_crud_operations(token)
    else:
        print_error("Não foi possível autenticar. Pulando testes autenticados.")
    
    # 6. Resumo final
    print_summary(all_results)
    
    print(f"\n{Colors.CYAN}🏁 Finalizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Teste interrompido pelo usuário{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}💥 Erro fatal: {str(e)}{Colors.END}")
        sys.exit(1)
