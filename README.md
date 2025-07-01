# 🏥 API de Gerenciamento de Clínicas Veterinárias

Sistema completo para gerenciar clínicas veterinárias, veterinários, tutores, pets e atendimentos.

## 🚀 Tecnologias Utilizadas

### **Tecnologias Obrigatórias Implementadas:**
- ✅ **PostgreSQL** - Banco de dados relacional
- ✅ **SQLAlchemy** - ORM com declarative base
- ✅ **FastAPI** - Framework web moderno e rápido
- ✅ **Pydantic** - Validação de dados e serialização
- ✅ **Swagger** - Documentação automática da API
- ✅ **JSON** - Comunicação via API REST

### **Dependências:**
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `sqlalchemy` - ORM
- `psycopg2-binary` - Driver PostgreSQL
- `pydantic` - Validação de dados
- `pydantic-settings` - Configurações com validação

## 📋 Estrutura do Projeto

```
veterinaria_project/
├── api/
│   ├── routes.py          # Endpoints da API
│   └── __init__.py
├── models/
│   ├── models.py          # Modelos SQLAlchemy
│   └── __init__.py
├── services/
│   ├── schemas.py         # Schemas Pydantic
│   ├── veterinario_service.py
│   └── __init__.py
├── repository/
│   ├── crud.py           # Operações CRUD
│   └── __init__.py
├── config.py             # Configurações da aplicação
├── database.py           # Configuração do banco
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências
├── .env.example         # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```

## 🏗️ Modelo de Dados

### **Entidades Principais:**

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
- `clinica_id` - Clínica onde trabalha

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
- `tutor_id` - Tutor responsável

#### **Atendimento**
- `id` - Identificador único
- `data` - Data e hora do atendimento
- `descricao` - Descrição do atendimento
- `pet_id` - Pet atendido
- `veterinario_id` - Veterinário responsável

## 🔗 Relacionamentos

- **Clínica** → **Veterinários** (1:N)
- **Veterinário** → **Atendimentos** (1:N)
- **Tutor** → **Pets** (1:N)
- **Pet** → **Atendimentos** (1:N)

## ⚙️ Configuração e Execução

### 1. **Configurar Banco PostgreSQL**
```bash
# Criar banco de dados
createdb veterinaria_db
```

### 2. **Configurar Variáveis de Ambiente**
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost/veterinaria_db
```

### 3. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

### 4. **Executar a Aplicação**
```bash
uvicorn main:app --reload
```

### 5. **Acessar Documentação**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 📚 Endpoints da API

### **Clínicas**
- `POST /api/clinicas` - Cadastrar nova clínica
- `GET /api/clinicas` - Listar todas as clínicas
- `GET /api/clinicas/{id}` - Buscar clínica específica
- `GET /api/clinicas/{id}/veterinarios` - Listar veterinários da clínica

### **Veterinários**
- `POST /api/veterinarios` - Cadastrar novo veterinário
- `GET /api/veterinarios` - Listar todos os veterinários
- `GET /api/veterinarios/{id}/atendimentos` - Listar atendimentos do veterinário

### **Tutores**
- `POST /api/tutores` - Cadastrar novo tutor
- `GET /api/tutores/{id}/pets` - Listar pets do tutor

### **Pets**
- `POST /api/pets` - Cadastrar novo pet
- `GET /api/pets` - Listar todos os pets
- `GET /api/pets/{id}/atendimentos` - Histórico de atendimentos do pet

### **Atendimentos**
- `POST /api/atendimentos` - Registrar novo atendimento
- `GET /api/atendimentos` - Listar todos os atendimentos

## 🎯 Funcionalidades

- ✅ **CRUD completo** para todas as entidades
- ✅ **Validação de dados** com Pydantic
- ✅ **Relacionamentos** entre entidades
- ✅ **Documentação automática** com Swagger
- ✅ **Tratamento de erros** HTTP
- ✅ **Configuração flexível** via variáveis de ambiente
- ✅ **Estrutura modular** e escalável

## 🔧 Desenvolvimento

O projeto segue as melhores práticas de desenvolvimento:
- Separação de responsabilidades
- Validação de entrada rigorosa
- Tratamento adequado de erros
- Documentação automática
- Configuração externalizável
- Código limpo e bem estruturado

---

**Desenvolvido com FastAPI + PostgreSQL + SQLAlchemy** 🚀
