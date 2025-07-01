# 🚀 Comandos Úteis - API Veterinária

## 📦 Instalação e Configuração

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Inicializar banco de dados
python init_db.py

# 3. Popular com dados de exemplo (opcional)
python populate_db.py

# 4. Executar servidor de desenvolvimento
python -m uvicorn main:app --reload
```

## 🌐 URLs Importantes

- **API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **API Root**: http://127.0.0.1:8000/
- **OpenAPI JSON**: http://127.0.0.1:8000/api/openapi.json

## 🧪 Testes Rápidos via Swagger

### 1. Testar Clínicas
```bash
GET /api/clinicas - Listar todas as clínicas
GET /api/clinicas/1 - Buscar clínica específica
POST /api/clinicas - Criar nova clínica
```

### 2. Testar Veterinários
```bash
GET /api/veterinarios - Listar veterinários
POST /api/veterinarios - Cadastrar veterinário
GET /api/clinicas/1/veterinarios - Veterinários de uma clínica
```

### 3. Testar Pets e Tutores
```bash
GET /api/pets - Listar pets
POST /api/tutores - Cadastrar tutor
POST /api/pets - Cadastrar pet
```

### 4. Testar Atendimentos
```bash
GET /api/atendimentos - Listar atendimentos
POST /api/atendimentos - Registrar atendimento
GET /api/pets/1/atendimentos - Histórico do pet
```

## 🗄️ Banco de Dados

### SQLite (Desenvolvimento)
- Arquivo: `veterinaria.db`
- Configuração automática
- Ideal para testes locais

### PostgreSQL (Produção)
```bash
# Configurar no .env
DATABASE_URL=postgresql://usuario:senha@localhost/veterinaria_db
```

## 🔧 Desenvolvimento

### Estrutura de Pastas
```
├── api/routes.py      # Endpoints FastAPI
├── models/models.py   # Modelos SQLAlchemy
├── services/schemas.py # Validação Pydantic
├── repository/crud.py # Operações CRUD
├── database.py        # Configuração DB
├── main.py           # App principal
└── config.py         # Configurações
```

### Scripts Úteis
- `init_db.py` - Inicializar banco
- `populate_db.py` - Dados de exemplo
- `main.py` - Servidor principal

## 📝 Exemplos de JSON

### Criar Clínica
```json
{
  "nome": "Clínica VetLife",
  "cidade": "São Paulo",
  "endereco": "Rua das Flores, 123"
}
```

### Criar Veterinário
```json
{
  "nome": "Dr. João Silva",
  "crmv": "SP-12345",
  "email": "joao@email.com",
  "especialidade": "Clínica Geral",
  "clinica_id": 1
}
```

### Criar Pet
```json
{
  "nome": "Rex",
  "especie": "Cão",
  "raca": "Golden Retriever",
  "idade": 3,
  "tutor_id": 1
}
```
