# 🏥 API de Gerenciamento de Clínicas Veterinárias

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17+-blue.svg)](https://postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://sqlalchemy.org)

Sistema completo para gerenciar clínicas veterinárias, veterinários, tutores, pets e atendimentos desenvolvido com FastAPI, PostgreSQL e SQLAlchemy.

## 📋 Índice

- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação](#-autenticação)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Banco de Dados](#-banco-de-dados)
- [Desenvolvimento](#-desenvolvimento)
- [Deploy](#-deploy)

## 🚀 Tecnologias

### **Tecnologias Obrigatórias Implementadas:**
- ✅ **PostgreSQL 17** - Banco de dados relacional
- ✅ **SQLAlchemy 2.0** - ORM com declarative base
- ✅ **FastAPI** - Framework web moderno e rápido
- ✅ **Pydantic V2** - Validação de dados e serialização
- ✅ **Swagger/OpenAPI** - Documentação automática da API
- ✅ **JSON** - Comunicação via API REST

### **Dependências Principais:**
```
fastapi==0.104.1              # Framework web
uvicorn[standard]==0.24.0      # Servidor ASGI
sqlalchemy==2.0.23            # ORM
psycopg2-binary==2.9.9         # Driver PostgreSQL
pydantic==2.5.0               # Validação de dados
pydantic-settings==2.1.0      # Configurações
python-jose[cryptography]==3.3.0  # JWT tokens
passlib[bcrypt]==1.7.4         # Hash de senhas
bcrypt==4.0.1                  # Algoritmo de hash
```

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### 1. **Python 3.11+**
```bash
# Verificar versão
python --version
```

### 2. **PostgreSQL 17**
- **Windows**: [Download PostgreSQL](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

### 3. **Git**
```bash
# Verificar se está instalado
git --version
```

## 🔧 Instalação e Configuração

### 1. **Clonar o repositório**
```bash
git clone https://github.com/arleswasb/veterinaria-api.git
cd veterinaria-api
```
### 2. **Ativar o docker desktop**
```bash
##########
```

### 3. **Criar ambiente virtual (recomendado)**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\Activate.ps1
#Linux
source venv/bin/activate
```

### 4. **Instalar dependências**
```bash

pip install -r requirements.txt

uvicorn main:app --reload
```

### 5. **Configurar PostgreSQL**
```
###**Abra um novo terminal**
```

#### Opção A: Configuração Automática
```bash
python setup_postgres.py
```

#### Opção B: Configuração Manual
```sql
-- Conectar ao PostgreSQL como superusuário
psql -U postgres

-- Criar banco de dados
CREATE DATABASE veterinaria_db;

-- Verificar criação
\l
\q
```

### 6. **Configurar variáveis de ambiente**
```bash
# Copiar arquivo de exemplo
cp .env.example .env
```

**Conteúdo do `.env`:**
```env
# Configurações do banco de dados
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/veterinaria_db

# Configurações da aplicação
ENVIRONMENT=production
DEBUG=true
APP_NAME="API de Gerenciamento de Clínicas Veterinárias"
APP_VERSION="1.0.0"

# Configurações PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SUA_SENHA
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=veterinaria_db
```

### 7. **Inicializar banco de dados**
```bash
# Criar tabelas
python init_db.py

# Popular com dados de exemplo (opcional)
python populate_db.py
```

## 🚀 Como Executar

### 1. **Executar servidor de desenvolvimento**
```bash
# Método 1: Uvicorn direto
python -m uvicorn main:app --reload

# Método 2: Com host e porta específicos
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Método 3: Com configurações de produção
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. **Verificar se está funcionando**
- **API Root**: http://127.0.0.1:8000/
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### 3. **Parar o servidor**
```bash
# Pressionar Ctrl+C no terminal
```

## 📁 Estrutura do Projeto

```
veterinaria_project/
├── 📁 api/
│   ├── __init__.py
│   └── routes.py              # 🛣️  Endpoints REST API
├── 📁 models/
│   ├── __init__.py
│   └── models.py              # 🗃️  Modelos SQLAlchemy ORM
├── 📁 services/
│   ├── __init__.py
│   ├── schemas.py             # ✅ Schemas Pydantic
│   └── veterinario_service.py # 🔧 Regras de negócio
├── 📁 repository/
│   ├── __init__.py
│   └── crud.py                # 🔄 Operações CRUD
├── 📄 config.py               # ⚙️  Configurações
├── 📄 database.py             # 🗃️  Configuração do banco
├── 📄 main.py                 # 🚀 Aplicação principal
├── 📄 init_db.py              # 🔨 Script inicializar DB
├── 📄 populate_db.py          # 🌱 Script dados exemplo
├── 📄 setup_postgres.py       # 🐘 Setup PostgreSQL
├── 📄 requirements.txt        # 📦 Dependências
├── 📄 .env.example           # 🔧 Exemplo configurações
├── 📄 .gitignore             # 🚫 Arquivos ignorados
└── 📄 README.md              # 📖 Documentação
```

## 🌐 Endpoints da API

### **🔐 Autenticação**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/register` | Registrar novo usuário |
| `POST` | `/api/token` | Login e obter token JWT |
| `GET` | `/api/users/me` | Obter dados do usuário autenticado |

### **🏥 Clínicas**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/clinicas` | Cadastrar nova clínica (requer autenticação) |
| `GET` | `/api/clinicas` | Listar todas as clínicas |
| `GET` | `/api/clinicas/{id}` | Buscar clínica específica |
| `GET` | `/api/clinicas/{id}/veterinarios` | Listar veterinários da clínica |

### **👩‍⚕️ Veterinários**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/veterinarios` | Cadastrar novo veterinário |
| `GET` | `/api/veterinarios` | Listar todos os veterinários |
| `GET` | `/api/veterinarios/{id}/atendimentos` | Listar atendimentos do veterinário |

### **👨‍👩‍👧‍👦 Tutores**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/tutores` | Cadastrar novo tutor |
| `GET` | `/api/tutores/{id}/pets` | Listar pets do tutor |

### **🐕 Pets**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/pets` | Cadastrar novo pet |
| `GET` | `/api/pets` | Listar todos os pets |
| `GET` | `/api/pets/{id}/atendimentos` | Histórico de atendimentos do pet |

### **📋 Atendimentos**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/atendimentos` | Registrar novo atendimento |
| `GET` | `/api/atendimentos` | Listar todos os atendimentos |

## 🔐 Autenticação

O sistema implementa autenticação JWT para proteger endpoints sensíveis. 

### **Usuários de Exemplo:**
- **admin** / **admin123** - Usuário administrador
- **demo** / **demo123** - Usuário de demonstração

### **Fluxo de Autenticação:**
1. **Registrar** novo usuário via `/api/register`
2. **Fazer login** via `/api/token` para obter token JWT
3. **Usar token** no header `Authorization: Bearer {token}` para acessar endpoints protegidos

### **Documentação Completa:**
📖 Veja o arquivo [AUTHENTICATION.md](./AUTHENTICATION.md) para guia completo de autenticação com exemplos práticos.

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

### **Estrutura de Desenvolvimento**
```bash
# Executar em modo desenvolvimento
python -m uvicorn main:app --reload

# Executar testes (quando implementados)
pytest

# Verificar estilo de código
flake8 .

# Formatar código
black .
```

### **Adicionar Nova Funcionalidade**
1. **Criar modelo** em `models/models.py`
2. **Criar schema** em `services/schemas.py`
3. **Adicionar CRUD** em `repository/crud.py`
4. **Criar endpoint** em `api/routes.py`
5. **Testar** via Swagger UI

### **Scripts Utilitários**
```bash
# Verificar status do banco
python setup_postgres.py status

# Recriar banco (cuidado!)
python init_db.py

# Popular dados de exemplo
python populate_db.py

# Verificar configurações
python -c "from config import settings; print(settings.effective_database_url)"
```

## 🚀 Deploy

### **Docker (Recomendado)**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_DB: veterinaria_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: senha_segura
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://postgres:senha_segura@db:5432/veterinaria_db

volumes:
  postgres_data:
```

### **Heroku**
```bash
# Instalar Heroku CLI e fazer login
heroku login

# Criar app
heroku create veterinaria-api

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main
```

### **Railway/Render**
1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Deploy automático

## 🛠️ Solução de Problemas

### **Erro de Conexão PostgreSQL**
```bash
# Verificar se PostgreSQL está rodando
# Windows
services.msc (procurar postgresql)

# macOS  
brew services list | grep postgres

# Linux
sudo systemctl status postgresql

# Verificar porta
netstat -an | findstr 5432
```

### **Erro "Table doesn't exist"**
```bash
# Recriar tabelas
python init_db.py
```

### **Erro de dependências**
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### **Erro de encoding**
```bash
# Verificar encoding do terminal
chcp 65001  # Windows
export LANG=en_US.UTF-8  # Linux/macOS
```

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/arleswasb/veterinaria-api/issues)
- **Documentação**: http://127.0.0.1:8000/docs
- **Email**: (adicione seu email aqui)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**🎉 Desenvolvido com FastAPI + PostgreSQL + SQLAlchemy**
