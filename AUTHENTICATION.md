# 🔐 Guia de Autenticação - API Veterinária

## Visão Geral

A API implementa autenticação JWT (JSON Web Tokens) para proteger endpoints que requerem identificação do usuário. O sistema utiliza:

- **JWT Tokens** para autenticação stateless
- **Hash bcrypt** para armazenamento seguro de senhas  
- **OAuth2 Password Flow** para obtenção de tokens

## Endpoints de Autenticação

### 1. Registro de Usuário

**POST** `/api/register`

Registra um novo usuário no sistema.

**Request Body:**
```json
{
  "username": "joao123",
  "email": "joao@email.com", 
  "password": "minhasenha123"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "joao123",
  "email": "joao@email.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 2. Login e Obtenção de Token

**POST** `/api/token`

Autentica o usuário e retorna um token JWT.

**Request Body (form-data):**
```
username=joao123&password=minhasenha123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Obter Perfil do Usuário

**GET** `/api/users/me`

Retorna informações do usuário autenticado.

**Headers:**
```
Authorization: Bearer {seu_token_aqui}
```

**Response:**
```json
{
  "id": 1,
  "username": "joao123", 
  "email": "joao@email.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

## Como Usar Autenticação

### 1. PowerShell

**Registrar usuário:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/register" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"username": "teste", "email": "teste@teste.com", "password": "teste123"}'
```

**Fazer login:**
```powershell
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/token" `
  -Method POST `
  -Headers @{"Content-Type"="application/x-www-form-urlencoded"} `
  -Body "username=teste&password=teste123"

$token = $response.access_token
```

**Usar token em requisições protegidas:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/clinicas" `
  -Method POST `
  -Headers @{
    "Content-Type"="application/json"
    "Authorization"="Bearer $token"
  } `
  -Body '{"nome": "Clínica Teste", "cidade": "São Paulo", "endereco": "Rua Teste, 123"}'
```

### 2. cURL (Linux/macOS)

**Registrar usuário:**
```bash
curl -X POST "http://127.0.0.1:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "teste", "email": "teste@teste.com", "password": "teste123"}'
```

**Fazer login:**
```bash
curl -X POST "http://127.0.0.1:8000/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste&password=teste123"
```

**Usar token:**
```bash
TOKEN="seu_token_aqui"
curl -X POST "http://127.0.0.1:8000/api/clinicas" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"nome": "Clínica Teste", "cidade": "São Paulo", "endereco": "Rua Teste, 123"}'
```

### 3. Python

```python
import requests

# Registrar usuário
register_data = {
    "username": "teste",
    "email": "teste@teste.com", 
    "password": "teste123"
}
response = requests.post("http://127.0.0.1:8000/api/register", json=register_data)
print(response.json())

# Fazer login
login_data = {"username": "teste", "password": "teste123"}
response = requests.post("http://127.0.0.1:8000/api/token", data=login_data)
token = response.json()["access_token"]

# Usar token
headers = {"Authorization": f"Bearer {token}"}
clinica_data = {
    "nome": "Clínica Teste",
    "cidade": "São Paulo", 
    "endereco": "Rua Teste, 123"
}
response = requests.post("http://127.0.0.1:8000/api/clinicas", 
                        json=clinica_data, headers=headers)
print(response.json())
```

## Endpoints Protegidos

Os seguintes endpoints requerem autenticação:

- `POST /api/clinicas` - Criar clínica
- (Outros endpoints podem ser protegidos conforme necessário)

## Configurações de Token

- **Duração**: 30 minutos (configurável via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Algoritmo**: HS256
- **Chave Secreta**: Configurável via `SECRET_KEY` no arquivo `.env`

## Códigos de Erro

- **400**: Username ou email já registrado
- **401**: Credenciais inválidas ou token expirado
- **422**: Dados de entrada inválidos

## Usuários de Exemplo

Se você executou `python populate_db.py`, existem dois usuários de exemplo:

- **Username**: `admin` | **Senha**: `admin123`
- **Username**: `demo` | **Senha**: `demo123`

## Segurança

### Boas Práticas Implementadas:

1. **Hash de Senhas**: Senhas são hasheadas com bcrypt
2. **Tokens JWT**: Autenticação stateless e segura
3. **Validação de Email**: Formato de email validado
4. **Usernames Únicos**: Prevenção de duplicatas
5. **Expiração de Token**: Tokens expiram em 30 minutos

### Recomendações para Produção:

1. **Altere a SECRET_KEY**: Use uma chave aleatória e segura
2. **HTTPS**: Use sempre HTTPS em produção
3. **Validação de Senha**: Implemente regras de senha forte
4. **Rate Limiting**: Limite tentativas de login
5. **Logs de Auditoria**: Registre tentativas de acesso

## Troubleshooting

### Token Inválido ou Expirado
```json
{
  "detail": "Could not validate credentials"
}
```
**Solução**: Faça login novamente para obter um novo token.

### Username já Existe
```json
{
  "detail": "Username já está registrado"
}
```
**Solução**: Use um username diferente.

### Email já Existe  
```json
{
  "detail": "Email já está registrado"
}
```
**Solução**: Use um email diferente.
