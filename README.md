# 🏥 API de Gerenciamento de Clínicas Veterinárias

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)

Sistema completo para gerenciar clínicas veterinárias, veterinários, tutores, pets e atendimentos desenvolvido com **FastAPI**, **PostgreSQL** e **SQLAlchemy**. Arquitetura modular e escalável com suporte completo a **Docker**.

## 🎯 **Características Principais**

- ✅ **API REST Completa** com documentação automática Swagger/OpenAPI
- ✅ **Autenticação JWT** com sistema de usuários seguro
- ✅ **Arquitetura Modular** seguindo padrões Clean Architecture
- ✅ **Containerização Docker** para deploy simplificado
- ✅ **Sistema de Validação** robusto com tratamento de erros
- ✅ **Logging Estruturado** para monitoramento e debug
- ✅ **Scripts de Automação** para setup e testes
- ✅ **Configuração Flexível** com suporte a múltiplos ambientes

## 📋 Índice

- [Características Principais](#-características-principais)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Docker Setup](#-docker-setup)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação](#-autenticação)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Banco de Dados](#-banco-de-dados)
- [Testes](#-testes)
- [Desenvolvimento](#-desenvolvimento)
- [Deploy](#-deploy)
- [Solução de Problemas](#-solução-de-problemas)

## 🚀 Tecnologias

### **Stack Principal:**
- ✅ **FastAPI 0.104.1** - Framework web moderno e rápido
- ✅ **PostgreSQL 16+** - Banco de dados relacional robusto
- ✅ **SQLAlchemy 2.0** - ORM com declarative base
- ✅ **Pydantic V2** - Validação de dados e serialização
- ✅ **Python 3.11+** - Linguagem base com tipagem moderna

### **Segurança & Autenticação:**
- 🔐 **JWT (JSON Web Tokens)** - Autenticação stateless
- 🔐 **bcrypt** - Hash seguro de senhas
- 🔐 **OAuth2 Password Flow** - Padrão de autenticação
- 🔐 **Pydantic Validation** - Validação robusta de dados

### **DevOps & Containerização:**
- 🐳 **Docker** - Containerização completa
- 🐳 **Docker Compose** - Orquestração de serviços
- 🛠️ **Uvicorn** - Servidor ASGI para produção
- 📊 **Logging** - Sistema de logs estruturado

### **Dependências Principais:**
```txt
# FastAPI e servidor ASGI
fastapi==0.116.0              # Framework web moderno
uvicorn[standard]==0.35.0     # Servidor ASGI

# Banco de dados
sqlalchemy==2.0.41           # ORM avançado
psycopg2-binary==2.9.10      # Driver PostgreSQL

# Validação e configurações
pydantic==2.11.7             # Validação de dados
pydantic-settings==2.10.1    # Configurações
email-validator==2.2.0       # Validação de email

# Autenticação e segurança
python-jose[cryptography]==3.5.0  # JWT tokens
passlib[bcrypt]==1.7.4        # Hash de senhas
bcrypt==4.3.0                 # Algoritmo de hash

# Utilidades
python-multipart==0.0.20     # Upload de formulários
python-dotenv==1.1.1         # Variáveis de ambiente
requests==2.32.3             # Cliente HTTP para testes
```

## 📦 **Gestão de Dependências**

### **Estrutura de Arquivos:**
```
📦 Dependências organizadas por ambiente:
├── 📄 requirements.txt        # ✅ Principais + desenvolvimento
├── 📄 requirements-prod.txt   # 🏭 Apenas produção (otimizado)
├── 📄 requirements-dev.txt    # 🛠️ Desenvolvimento completo
├── 📄 pyproject.toml         # ⚙️ Configuração moderna do projeto
└── 📄 .pre-commit-config.yaml # 🔍 Hooks de qualidade de código
```

### **Comandos de Instalação:**
```bash
# Desenvolvimento local
pip install -r requirements.txt

# Desenvolvimento com todas as ferramentas
pip install -r requirements-dev.txt

# Produção (Docker/Deploy)
pip install -r requirements-prod.txt

# Instalação moderna com pip
pip install -e ".[dev]"  # Com ferramentas de desenvolvimento
pip install -e ".[prod]" # Para produção
```

### **Ferramentas de Qualidade:**
```bash
# Configurar hooks de pré-commit
pre-commit install

# Executar todas as verificações
pre-commit run --all-files

# Verificações individuais
black .                    # Formatação
flake8 .                   # Linting
mypy .                     # Verificação de tipos
pytest                     # Testes
safety check              # Vulnerabilidades
bandit -r .               # Segurança
```

### **Dependências por Categoria:**

#### **🚀 Runtime (Produção)**
- **FastAPI 0.116.0** - Framework web
- **SQLAlchemy 2.0.41** - ORM 
- **PostgreSQL 2.9.10** - Driver de banco
- **Pydantic 2.11.7** - Validação
- **JWT + bcrypt** - Autenticação

#### **🛠️ Desenvolvimento**
- **Black 24.12.0** - Formatação de código
- **Flake8 7.1.1** - Linting
- **MyPy 1.14.1** - Verificação de tipos
- **Pytest 8.3.4** - Framework de testes
- **Pre-commit 4.0.1** - Hooks de qualidade

#### **🔍 Qualidade e Segurança**
- **Safety 3.3.1** - Scan de vulnerabilidades
- **Bandit 1.8.0** - Análise de segurança
- **Coverage** - Cobertura de testes
- **isort** - Organização de imports
```

## 🏗️ Arquitetura

### **Padrão Clean Architecture:**
```
📁 Presentation Layer     → api/routers/          (HTTP Endpoints)
📁 Business Layer        → services/             (Regras de Negócio)
📁 Data Access Layer     → crud/ + repository/   (Operações CRUD)
📁 Domain Layer          → models/ + schemas/    (Entidades e DTOs)
📁 Infrastructure Layer  → database.py + config.py (Configurações)
```

### **Separação de Responsabilidades:**
- **Routers** - Endpoints HTTP e validação de entrada
- **Services** - Lógica de negócio e orchestração
- **CRUD/Repository** - Operações de banco de dados
- **Models** - Entidades do domínio (SQLAlchemy)
- **Schemas** - DTOs e validação (Pydantic)
- **Config** - Configurações e variáveis de ambiente

## 📋 Pré-requisitos

### **Opção 1: Docker (Recomendado)**
```bash
# Apenas Docker e Docker Compose
docker --version
docker-compose --version
```

### **Opção 2: Instalação Manual**

#### 1. **Python 3.11+**
```bash
# Verificar versão
python --version
```

#### 2. **PostgreSQL 16+**
- **Windows**: [Download PostgreSQL](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

#### 3. **Git**
```bash
# Verificar se está instalado
git --version
```

## 🔧 Instalação e Configuração

### **Passo 1: Clonar o Repositório**
```bash
git clone https://github.com/arleswasb/veterinaria-api.git
cd veterinaria-api
```

### **Passo 2: Configurar Variáveis de Ambiente**
```bash
# Criar arquivo de configuração
cp .env.example .env
```

**Conteúdo do `.env`:**
```env
# Configurações do banco de dados
DATABASE_URL=postgresql://postgres:veterinaria123@localhost:5432/veterinaria_db

# Configurações PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=veterinaria123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=veterinaria_db

# Configurações da aplicação
ENVIRONMENT=development
DEBUG=true
APP_NAME="API de Gerenciamento de Clínicas Veterinárias"
APP_VERSION="2.0.0"

# Configurações JWT
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🐳 Docker Setup

### **Método 1: Docker Compose (Recomendado)**
```bash
# Construir e iniciar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f app
```

### **Método 2: Docker Manual**
```bash
# Construir imagem
docker build -t veterinaria-api .

# Executar PostgreSQL
docker run -d --name veterinaria-db \
  -e POSTGRES_DB=veterinaria_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=veterinaria123 \
  -p 5432:5432 \
  postgres:16-alpine

# Executar aplicação
docker run -d --name veterinaria-app \
  --link veterinaria-db:db \
  -p 8000:8000 \
  veterinaria-api
```

## 🔧 Instalação Manual

### **Passo 3: Criar Ambiente Virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate
```

### **Passo 4: Instalar Dependências**
```bash
# Opção 1: Instalação básica (recomendado para começar)
pip install -r requirements.txt

# Opção 2: Instalação para desenvolvimento (inclui ferramentas)
pip install -r requirements-dev.txt

# Opção 3: Instalação para produção (apenas essenciais)
pip install -r requirements-prod.txt

# Opção 4: Instalação individual (se necessário)
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic email-validator
```

### **Passo 5: Configurar PostgreSQL**

#### **Opção A: Configuração Automática**
```bash
python setup_postgres.py
```

#### **Opção B: Configuração Manual**
```sql
-- Conectar ao PostgreSQL
psql -U postgres

-- Criar banco de dados
CREATE DATABASE veterinaria_db;

-- Verificar criação
\l
\q
```

### **Passo 6: Inicializar e Popular Banco**
```bash
# Criar tabelas e popular com dados de exemplo
python populate_db.py

# Ou apenas criar tabelas
python init_db.py
```

## 🚀 Como Executar

### **Método 1: Docker Compose (Recomendado)**
```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Parar serviços
docker-compose down
```

### **Método 2: Instalação Manual**
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
# venv\Scripts\Activate.ps1  # Windows

# Executar servidor de desenvolvimento
python -m uvicorn main:app --reload

# Executar com configurações específicas
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Método 3: Validação de Startup**
```bash
# Validar configuração antes de executar
python validate_startup.py

# Se todas as validações passarem, executar
python -m uvicorn main:app --reload
```

### **Verificar se está funcionando**
- **🏠 API Root**: http://127.0.0.1:8000/
- **📋 Health Check**: http://127.0.0.1:8000/api/health
- **📖 Swagger UI**: http://127.0.0.1:8000/docs
- **📚 ReDoc**: http://127.0.0.1:8000/redoc

### **Parar o servidor**
```bash
# Pressionar Ctrl+C no terminal
# Ou para Docker:
docker-compose down
```

## 📁 Estrutura do Projeto

```
veterinaria-api/
├── 📁 api/                    # 🛣️ Camada de Apresentação
│   ├── routers/              # 🎯 Endpoints organizados por domínio
│   │   ├── auth.py          # 🔐 Autenticação e autorização
│   │   ├── clinicas.py      # 🏥 Endpoints de clínicas
│   │   ├── veterinarios.py  # 👩‍⚕️ Endpoints de veterinários
│   │   ├── tutores.py       # 👨‍👩‍👧‍👦 Endpoints de tutores
│   │   ├── pets.py          # � Endpoints de pets
│   │   └── atendimentos.py  # 📋 Endpoints de atendimentos
│   ├── exception_handlers.py # ⚠️ Tratamento de exceções
│   └── routes.py            # 🛣️ Agregador de rotas
├── 📁 schemas/               # ✅ Camada de Validação (DTOs)
│   ├── usuario.py           # 👤 Schemas de usuário
│   ├── clinica.py           # 🏥 Schemas de clínica
│   ├── veterinario.py       # 👩‍⚕️ Schemas de veterinário
│   ├── tutor.py             # 👨‍👩‍👧‍👦 Schemas de tutor
│   ├── pet.py               # 🐕 Schemas de pet
│   ├── atendimento.py       # 📋 Schemas de atendimento
│   └── token.py             # 🔑 Schemas de autenticação
├── 📁 models/                # 🗃️ Camada de Domínio
│   └── models.py            # 🏗️ Entidades SQLAlchemy
├── 📁 crud/                  # 🔄 Camada de Acesso a Dados
│   ├── usuario.py           # 👤 Operações CRUD usuário
│   ├── clinica.py           # 🏥 Operações CRUD clínica
│   ├── pet.py               # 🐕 Operações CRUD pet
│   ├── tutor.py             # 👨‍👩‍👧‍👦 Operações CRUD tutor
│   └── atendimento.py       # 📋 Operações CRUD atendimento
├── 📁 services/              # 🔧 Camada de Negócio
│   ├── auth.py              # 🔐 Serviços de autenticação
│   ├── dependencies.py      # 🔗 Dependências injetáveis
│   ├── veterinario_service.py # �‍⚕️ Regras de negócio
│   └── atendimento_service.py # 📋 Regras de negócio
├── 📁 repository/            # 🗂️ Camada de Repositório (Legacy)
│   └── crud.py              # 🔄 Operações CRUD centralizadas
├── 📄 main.py               # 🚀 Aplicação FastAPI
├── 📄 config.py             # ⚙️ Configurações da aplicação
├── 📄 database.py           # 🗃️ Configuração do banco
├── 📄 init_db.py            # � Inicialização do banco
├── 📄 populate_db.py        # 🌱 População com dados exemplo
├── 📄 setup_postgres.py     # � Setup automático PostgreSQL
├── 📄 validate_startup.py   # ✅ Validação de inicialização
├── 📄 test_api.py           # 🧪 Testes de integração
├── 📄 Dockerfile           # 🐳 Configuração Docker
├── 📄 docker-compose.yml   # 🐳 Orquestração de containers
├── 📄 entrypoint.sh        # � Script de inicialização
├── 📄 requirements.txt     # 📦 Dependências Python
├── 📄 .env.example        # 🔧 Exemplo de configurações
├── 📄 AUTHENTICATION.md   # 🔐 Guia de autenticação
├── 📄 PASSO_A_PASSO_SWAGGER.txt # � Guia Swagger
└── 📄 README.md           # � Documentação principal
```

### **Evolução da Arquitetura:**
- **v1.0**: Arquitetura monolítica com CRUD centralizado
- **v2.0**: Arquitetura modular com separação por domínios
- **Futuro**: Microserviços com arquitetura hexagonal

## 🌐 Endpoints da API

### **🔐 Autenticação**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `POST` | `/api/register` | Registrar novo usuário | ❌ Público |
| `POST` | `/api/token` | Login e obter token JWT | ❌ Público |
| `GET` | `/api/users/me` | Obter dados do usuário autenticado | ✅ JWT |

### **🏥 Clínicas**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `POST` | `/api/clinicas` | Cadastrar nova clínica | ✅ JWT |
| `GET` | `/api/clinicas` | Listar todas as clínicas | ❌ Público |
| `GET` | `/api/clinicas/{id}` | Buscar clínica específica | ❌ Público |
| `GET` | `/api/clinicas/{id}/veterinarios` | Listar veterinários da clínica | ❌ Público |

### **👩‍⚕️ Veterinários**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `POST` | `/api/veterinarios` | Cadastrar novo veterinário | ❌ Público |
| `GET` | `/api/veterinarios` | Listar todos os veterinários | ❌ Público |
| `GET` | `/api/veterinarios/{id}/atendimentos` | Listar atendimentos do veterinário | ❌ Público |

### **👨‍👩‍👧‍👦 Tutores**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `POST` | `/api/tutores` | Cadastrar novo tutor | ❌ Público |
| `GET` | `/api/tutores` | Listar todos os tutores | ❌ Público |
| `GET` | `/api/tutores/{id}/pets` | Listar pets do tutor | ❌ Público |

### **🐕 Pets**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `POST` | `/api/pets` | Cadastrar novo pet | ❌ Público |
| `GET` | `/api/pets` | Listar todos os pets | ❌ Público |
| `GET` | `/api/pets/{id}` | Buscar pet específico | ❌ Público |
| `GET` | `/api/pets/{id}/atendimentos` | Histórico de atendimentos do pet | ❌ Público |

### **📋 Atendimentos**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `POST` | `/api/atendimentos` | Registrar novo atendimento | ❌ Público |
| `GET` | `/api/atendimentos` | Listar todos os atendimentos | ❌ Público |
| `GET` | `/api/atendimentos/{id}` | Buscar atendimento específico | ❌ Público |

### **🔧 Utilitários**
| Método | Endpoint | Descrição | Proteção |
|--------|----------|-----------|----------|
| `GET` | `/` | Informações da API | ❌ Público |
| `GET` | `/api/health` | Health check | ❌ Público |

## 🔐 Autenticação

O sistema implementa **autenticação JWT robusta** com middleware de segurança e tratamento de erros personalizado.

### **Características de Segurança:**
- 🔐 **JWT Tokens** com expiração configurável (30 min padrão)
- 🔐 **Hash bcrypt** para senhas (salt rounds: 12)
- 🔐 **Validação de dados** com Pydantic
- 🔐 **Middleware de autenticação** para endpoints protegidos
- 🔐 **Tratamento de exceções** personalizado

### **Usuários de Exemplo:**
Após executar `python populate_db.py`:
- **admin** / **admin123** - Usuário administrador
- **demo** / **demo123** - Usuário de demonstração

### **Fluxo de Autenticação:**
1. **Registrar** usuário via `POST /api/register`
2. **Login** via `POST /api/token` para obter token JWT
3. **Usar token** no header `Authorization: Bearer {token}`

### **Configuração JWT:**
```python
# config.py
SECRET_KEY = "sua-chave-secreta-aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### **Documentação Completa:**
📖 **[AUTHENTICATION.md](./AUTHENTICATION.md)** - Guia completo com exemplos em:
- 🔧 **PowerShell**
- 🐍 **Python**
- 📱 **curl**
- 🌐 **JavaScript**

## 📝 Exemplos de Uso

### **1. Registrar Usuário**
```bash
curl -X POST "http://127.0.0.1:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao123",
    "email": "joao@email.com",
    "password": "minhasenha123"
  }'
```

### **2. Fazer Login e Obter Token**
```bash
curl -X POST "http://127.0.0.1:8000/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **3. Criar Clínica (com autenticação)**
```bash
curl -X POST "http://127.0.0.1:8000/api/clinicas" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "nome": "Clínica VetLife",
    "cidade": "São Paulo", 
    "endereco": "Rua das Flores, 123"
  }'
```

### **4. Criar Veterinário**
```bash
curl -X POST "http://127.0.0.1:8000/api/veterinarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. João Silva",
    "crmv": "SP-12345",
    "email": "joao@email.com",
    "especialidade": "Clínica Geral",
    "clinica_id": 1
  }'
```

### **5. Criar Pet**
```bash
curl -X POST "http://127.0.0.1:8000/api/pets" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Rex",
    "especie": "Cão",
    "raca": "Golden Retriever", 
    "idade": 3,
    "tutor_id": 1
  }'
```

### **6. Listar Clínicas**
```bash
curl -X GET "http://127.0.0.1:8000/api/clinicas"
```

## 🧪 Testes

### **Testes de Integração**
```bash
# Executar testes automatizados da API
python test_api.py

# Validar inicialização antes dos testes
python validate_startup.py
```

### **Testes Manuais via Swagger**
1. **Acesse**: http://127.0.0.1:8000/docs
2. **Registre usuário**: `POST /api/register`
3. **Faça login**: `POST /api/token`
4. **Teste endpoints**: Use o token obtido

### **Testes com curl**
```bash
# Health check
curl -X GET "http://127.0.0.1:8000/api/health"

# Listar clínicas
curl -X GET "http://127.0.0.1:8000/api/clinicas"

# Registrar usuário
curl -X POST "http://127.0.0.1:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "teste", "email": "teste@email.com", "password": "teste123"}'
```

### **Cobertura de Testes:**
- ✅ **Autenticação** - Registro, login, validação de token
- ✅ **CRUD Completo** - Todas as entidades principais
- ✅ **Validação** - Campos obrigatórios e formatos
- ✅ **Relacionamentos** - Integridade referencial
- ✅ **Tratamento de Erros** - Respostas padronizadas

## 🗄️ Banco de Dados

### **Modelo de Dados**

#### **Usuário**
- `id` - Identificador único
- `username` - Nome de usuário (único)
- `email` - E-mail do usuário (único)
- `hashed_password` - Senha hasheada com bcrypt
- `is_active` - Status do usuário (ativo/inativo)
- `created_at` - Data de criação
- `updated_at` - Data de última atualização

#### **Clínica**
- `id` - Identificador único
- `nome` - Nome da clínica
- `endereco` - Endereço completo
- `cidade` - Cidade onde está localizada

#### **Veterinário**
- `id` - Identificador único
- `nome` - Nome do profissional
- `crmv` - Conselho Regional de Medicina Veterinária (único)
- `email` - E-mail profissional (único)
- `especialidade` - Área de especialização
- `clinica_id` - FK para Clínica

#### **Tutor**
- `id` - Identificador único
- `nome` - Nome do tutor
- `telefone` - Telefone de contato
- `email` - E-mail (único)
- `endereco` - Endereço do tutor

#### **Pet**
- `id` - Identificador único
- `nome` - Nome do animal
- `especie` - Tipo de animal
- `raca` - Raça específica
- `idade` - Idade do pet
- `tutor_id` - FK para Tutor

#### **Atendimento**
- `id` - Identificador único
- `data` - Data e hora do atendimento
- `descricao` - Descrição do atendimento
- `pet_id` - FK para Pet
- `veterinario_id` - FK para Veterinário

### **Relacionamentos**
- **Clínica** → **Veterinários** (1:N)
- **Veterinário** → **Atendimentos** (1:N)
- **Tutor** → **Pets** (1:N)
- **Pet** → **Atendimentos** (1:N)

### **Comandos Úteis PostgreSQL**
```sql
-- Conectar ao banco
psql -U postgres -d veterinaria_db

-- Listar tabelas
\dt

-- Ver dados de uma tabela
SELECT * FROM clinicas;

-- Ver estrutura de uma tabela
\d clinicas

-- Backup do banco
pg_dump -U postgres veterinaria_db > backup.sql
```

## 👨‍💻 Desenvolvimento

### **Estrutura de Desenvolvimento Moderna**
```bash
# Ambiente de desenvolvimento com hot-reload
python -m uvicorn main:app --reload

# Ambiente de desenvolvimento com Docker
docker-compose up -d
docker-compose logs -f app

# Executar testes durante desenvolvimento
python test_api.py
```

### **Adicionar Nova Funcionalidade**
1. **Criar Schema** em `schemas/{entidade}.py`
2. **Criar Modelo** em `models/models.py`
3. **Criar CRUD** em `crud/{entidade}.py`
4. **Criar Service** em `services/{entidade}_service.py` (se necessário)
5. **Criar Router** em `api/routers/{entidade}.py`
6. **Registrar Router** em `api/routes.py`
7. **Testar** via Swagger UI ou `test_api.py`

### **Padrões de Código**
```python
# Estrutura de um Router
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import entidade as schemas
from crud import entidade as crud

router = APIRouter(prefix="/entidade", tags=["entidade"])

@router.post("/", response_model=schemas.Entidade)
def create_entidade(entidade: schemas.EntidadeCreate, db: Session = Depends(get_db)):
    return crud.create_entidade(db=db, entidade=entidade)
```

### **Scripts de Desenvolvimento**
```bash
# Resetar banco de dados
python init_db.py

# Popular com dados de exemplo
python populate_db.py

# Validar configuração
python validate_startup.py

# Testar API completa
python test_api.py

# Verificar configurações
python -c "from config import settings; print(settings.effective_database_url)"
```

### **Ferramentas de Desenvolvimento**
```bash
# Instalar ferramentas de desenvolvimento
pip install -r requirements-dev.txt

# Formatação de código
black .
black --check .  # Verificar sem alterar

# Linting e análise estática
flake8 .
mypy .

# Testes unitários
pytest
pytest --cov=. --cov-report=html  # Com coverage

# Verificar segurança
safety check

# Análise de dependências
pip-audit  # Verificar vulnerabilidades
```

### **Configuração de Pré-commit (Opcional)**
```bash
# Instalar pré-commit hooks
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

### **Debugging**
```python
# main.py - Ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# Usar breakpoints
import pdb; pdb.set_trace()

# Logs estruturados
logger.info(f"Processando: {data}")
logger.error(f"Erro: {error}")
```

## 🚀 Deploy

### **🐳 Docker Compose (Recomendado)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: veterinaria_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: veterinaria123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env
    command: ./entrypoint.sh

volumes:
  postgres_data:
```

```bash
# Deploy completo
docker-compose up -d --build

# Monitorar logs
docker-compose logs -f app

# Backup do banco
docker exec veterinaria_db pg_dump -U postgres veterinaria_db > backup.sql
```

### **☁️ Heroku**
```bash
# Preparar Heroku
heroku login
heroku create veterinaria-api-prod

# Configurar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variáveis de ambiente
heroku config:set SECRET_KEY=sua-chave-super-segura
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=false

# Deploy
git push heroku main

# Executar migrações
heroku run python populate_db.py
```

### **🚀 Railway/Render**
1. **Conectar repositório GitHub**
2. **Configurar variáveis de ambiente**
3. **Configurar comando de build**: `pip install -r requirements.txt`
4. **Configurar comando de start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Deploy automático** a cada commit

### **🔧 Variáveis de Ambiente para Produção**
```env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=chave-super-segura-com-32-caracteres
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## 🛠️ Solução de Problemas

### **🐳 Problemas com Docker**
```bash
# Limpar containers e volumes
docker-compose down -v
docker system prune -a

# Reconstruir imagens
docker-compose up --build --force-recreate

# Ver logs específicos
docker-compose logs db
docker-compose logs app
```

### **🗄️ Problemas com PostgreSQL**
```bash
# Verificar se PostgreSQL está rodando
# Windows
services.msc (procurar postgresql)

# macOS
brew services list | grep postgres

# Linux
sudo systemctl status postgresql

# Verificar conexão
telnet localhost 5432
```

### **🐍 Problemas com Python**
```bash
# Verificar versão do Python
python --version

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Limpar cache do pip
pip cache purge

# Verificar ambiente virtual
which python
```

### **📊 Problemas com Banco de Dados**
```bash
# Recriar tabelas
python init_db.py

# Verificar dados
python -c "from database import engine; print(engine.execute('SELECT version()').fetchone())"

# Backup antes de recriar
pg_dump -U postgres veterinaria_db > backup.sql
```

### **🔧 Problemas de Configuração**
```bash
# Verificar variáveis de ambiente
python -c "from config import settings; print(settings.dict())"

# Testar configuração
python validate_startup.py

# Verificar encoding
# Windows
chcp 65001

# Linux/macOS
export LANG=en_US.UTF-8
```

### **⚠️ Erros Comuns**

#### **Erro: "Table doesn't exist"**
```bash
# Solução: Recriar tabelas
python init_db.py
```

#### **Erro: "Connection refused"**
```bash
# Solução: Verificar se PostgreSQL está rodando
# E se as credenciais estão corretas no .env
```

#### **Erro: "Module not found"**
```bash
# Solução: Instalar dependências
pip install -r requirements.txt
```

#### **Erro: "Port already in use"**
```bash
# Solução: Matar processo na porta 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### **🆘 Suporte**
- **📝 Issues**: [GitHub Issues](https://github.com/arleswasb/veterinaria-api/issues)
- **📖 Documentação**: http://127.0.0.1:8000/docs
- **🔍 Logs**: `docker-compose logs -f app`
- **🧪 Testes**: `python test_api.py`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🏆 **Sobre o Projeto**

**Versão**: 2.0.0  
**Última Atualização**: Janeiro 2025  
**Status**: ✅ Produção Ready

### **Tecnologias Utilizadas**
🐍 **Python 3.11+** | ⚡ **FastAPI** | 🐘 **PostgreSQL** | 🔧 **SQLAlchemy** | 🐳 **Docker**

### **Recursos Implementados**
- ✅ **API REST Completa** com 25+ endpoints
- ✅ **Autenticação JWT** com middleware de segurança
- ✅ **Arquitetura Modular** com separação de responsabilidades
- ✅ **Containerização Docker** com docker-compose
- ✅ **Documentação Swagger** interativa
- ✅ **Testes Automatizados** de integração
- ✅ **Tratamento de Erros** customizado
- ✅ **Logging Estruturado** para monitoramento
- ✅ **Scripts de Automação** para deploy e setup

### **Métricas do Projeto**
- 📁 **52 arquivos** organizados em estrutura modular
- 🛣️ **6 domínios** de API (Auth, Clínicas, Veterinários, Tutores, Pets, Atendimentos)
- 📋 **6 entidades** de banco de dados com relacionamentos
- 🔧 **25+ endpoints** REST documentados
- 🧪 **187 linhas** de testes automatizados
- 📖 **564 linhas** de documentação

**🎉 Desenvolvido com FastAPI + PostgreSQL + SQLAlchemy + Docker**
