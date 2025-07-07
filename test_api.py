#!/usr/bin/env python3
"""
Script de teste de integração para a API Veterinária.

Este script executa chamadas HTTP para os endpoints da API para verificar
as operações CRUD (Create, Read, Update, Delete) para as principais
entidades do sistema.

Pré-requisitos para executar:
1. A aplicação FastAPI deve estar em execução (ex: uvicorn main:app --reload).
2. O banco de dados deve ter sido populado (ex: python populate_db.py).
3. A biblioteca 'requests' deve estar instalada (pip install requests).
"""

import requests
import json
import sys

# --- Configuração ---
BASE_URL = "http://127.0.0.1:8000/api"
AUTH_TOKEN = None

def get_headers():
    """Retorna os cabeçalhos, incluindo o de autorização se o token existir."""
    headers = {"Content-Type": "application/json"}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    return headers

# --- Estado para armazenar IDs criados durante os testes ---
created_ids = {
    "clinica": None,
    "tutor": None,
    "pet": None,
    "veterinario": None,
}

def print_test_header(name):
    """Imprime um cabeçalho para um grupo de testes."""
    print("\n" + "="*10 + f" TESTANDO: {name} " + "="*10)

def run_test(description, method, url, expected_status, payload=None):
    """Função auxiliar para executar um teste e imprimir o resultado."""
    try:
        full_url = f"{BASE_URL}{url}"
        print(f" ▶️  {description:<50} [{method.upper()}] {url}", end="")
        
        # Usar application/x-www-form-urlencoded para o endpoint de token
        headers = get_headers()
        data = payload
        if url == "/auth/token":
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        elif payload:
            data = json.dumps(payload)

        response = requests.request(method, full_url, headers=headers, data=data)
        
        if response.status_code == expected_status:
            print(" -> ✅ SUCESSO")
            return response.json()
        else:
            print(f" -> ❌ FALHA (Esperado: {expected_status}, Recebido: {response.status_code})")
            try:
                print(f"      Resposta: {response.json()}")
            except json.JSONDecodeError:
                print(f"      Resposta: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print(f" -> ❌ FALHA (Erro de Conexão)")
        print("    Certifique-se de que a aplicação FastAPI está rodando em http://127.0.0.1:8000")
        sys.exit(1)
    except Exception as e:
        print(f" -> ❌ FALHA (Erro inesperado: {e})")
        return None

def test_health_check():
    print_test_header("Health Check")
    run_test("Verificando a saúde da API", "get", "/health", 200)

def test_authentication():
    global AUTH_TOKEN
    print_test_header("Autenticação")
    # Teste de falha (sem autenticação)
    run_test("Acessar rota protegida sem token", "get", "/clinicas/", 401)
    # Teste de login
    login_payload = {"username": "admin", "password": "admin123"}
    token_data = run_test("Realizar login para obter token", "post", "/auth/token", 200, payload=login_payload)
    if token_data and "access_token" in token_data:
        AUTH_TOKEN = token_data["access_token"]

def test_clinicas_crud():
    print_test_header("CRUD de Clínicas")
    clinica_payload = {"nome": "Clínica Teste API", "cidade": "Teste", "endereco": "Rua Teste, 123"}
    created = run_test("Criar nova clínica", "post", "/clinicas/", 201, payload=clinica_payload)
    if not created or "id" not in created: return
    
    item_id = created["id"]
    created_ids["clinica"] = item_id
    
    run_test(f"Buscar clínica por ID ({item_id})", "get", f"/clinicas/{item_id}", 200)
    run_test("Listar todas as clínicas", "get", "/clinicas/", 200)
    update_payload = {"nome": "Clínica Teste API Atualizada"}
    run_test(f"Atualizar clínica ({item_id})", "put", f"/clinicas/{item_id}", 200, payload=update_payload)
    run_test(f"Deletar clínica ({item_id})", "delete", f"/clinicas/{item_id}", 200)
    run_test(f"Verificar se clínica ({item_id}) foi deletada", "get", f"/clinicas/{item_id}", 404)

def test_tutores_crud():
    print_test_header("CRUD de Tutores")
    tutor_payload = {"nome": "Tutor Teste API", "telefone": "99999-9999", "email": "tutor.teste@api.com"}
    created = run_test("Criar novo tutor", "post", "/tutores/", 201, payload=tutor_payload)
    if not created or "id" not in created: return

    item_id = created["id"]
    created_ids["tutor"] = item_id

    run_test(f"Buscar tutor por ID ({item_id})", "get", f"/tutores/{item_id}", 200)
    run_test("Listar todos os tutores", "get", "/tutores/", 200)
    update_payload = {"nome": "Tutor Teste API Atualizado"}
    run_test(f"Atualizar tutor ({item_id})", "put", f"/tutores/{item_id}", 200, payload=update_payload)
    run_test(f"Deletar tutor ({item_id})", "delete", f"/tutores/{item_id}", 200)
    run_test(f"Verificar se tutor ({item_id}) foi deletado", "get", f"/tutores/{item_id}", 404)

def test_pets_crud():
    print_test_header("CRUD de Pets")
    tutor_id = created_ids.get("tutor")
    if not tutor_id:
        print("⚠️  Pulando testes de Pets pois a criação do Tutor de teste falhou.")
        return
        
    pet_payload = {"nome": "Pet Teste API", "especie": "Cachorro", "raca": "API Hound", "tutor_id": tutor_id}
    created = run_test("Criar novo pet", "post", "/pets/", 201, payload=pet_payload)
    if not created or "id" not in created: return

    item_id = created["id"]
    created_ids["pet"] = item_id

    run_test(f"Buscar pet por ID ({item_id})", "get", f"/pets/{item_id}", 200)
    run_test("Listar todos os pets", "get", "/pets/", 200)
    update_payload = {"nome": "Pet Teste API Atualizado", "idade": 1}
    run_test(f"Atualizar pet ({item_id})", "put", f"/pets/{item_id}", 200, payload=update_payload)
    run_test(f"Deletar pet ({item_id})", "delete", f"/pets/{item_id}", 200)
    run_test(f"Verificar se pet ({item_id}) foi deletado", "get", f"/pets/{item_id}", 404)

def test_veterinarios_crud():
    print_test_header("CRUD de Veterinários")
    # A clínica de teste já deve ter sido criada
    clinica_id = created_ids.get("clinica")
    if not clinica_id:
        print("⚠️  Pulando testes de Veterinários pois a criação da Clínica de teste falhou.")
        return

    vet_payload = {"nome": "Dr. Teste API", "crmv": "TEST-98765", "email": "vet.teste@api.com", "especialidade": "Testologia", "clinica_id": clinica_id}
    created = run_test("Criar novo veterinário", "post", "/veterinarios/", 201, payload=vet_payload)
    if not created or "id" not in created: return

    item_id = created["id"]
    created_ids["veterinario"] = item_id

    run_test(f"Buscar veterinário por ID ({item_id})", "get", f"/veterinarios/{item_id}", 200)

def test_atendimentos_crud():
    print_test_header("CRUD de Atendimentos")
    pet_id = created_ids.get("pet")
    vet_id = created_ids.get("veterinario")
    if not pet_id or not vet_id:
        print("⚠️  Pulando testes de Atendimentos pois a criação do Pet ou Veterinário de teste falhou.")
        return

    atendimento_payload = {"descricao": "Atendimento de Teste API", "pet_id": pet_id, "veterinario_id": vet_id}
    created = run_test("Criar novo atendimento", "post", "/atendimentos/", 201, payload=atendimento_payload)
    if not created or "id" not in created: return

    item_id = created["id"]
    run_test(f"Buscar atendimento por ID ({item_id})", "get", f"/atendimentos/{item_id}", 200)
    run_test(f"Deletar atendimento ({item_id})", "delete", f"/atendimentos/{item_id}", 200)
    run_test(f"Verificar se atendimento ({item_id}) foi deletado", "get", f"/atendimentos/{item_id}", 404)

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DE INTEGRAÇÃO DA API VETERINÁRIA 🚀")
    test_health_check()
    test_authentication()
    test_clinicas_crud()
    test_tutores_crud()
    test_pets_crud()
    test_veterinarios_crud()
    test_atendimentos_crud()
    print("\n" + "="*30 + "\n🏁 TESTES FINALIZADOS 🏁\n" + "="*30)