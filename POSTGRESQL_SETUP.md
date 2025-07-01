# 🐘 Configuração PostgreSQL - API Veterinária

## 📋 Pré-requisitos

### Windows
1. **Instalar PostgreSQL**
   ```bash
   # Opção 1: Download direto
   # https://www.postgresql.org/download/windows/
   
   # Opção 2: Via Chocolatey
   choco install postgresql
   
   # Opção 3: Via Scoop
   scoop install postgresql
   ```

2. **Configurar PATH** (se necessário)
   - Adicione `C:\Program Files\PostgreSQL\15\bin` às variáveis de ambiente

### macOS
```bash
# Via Homebrew
brew install postgresql
brew services start postgresql
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 🔧 Configuração Rápida

### 1. Verificar Status
```bash
# Verificar se PostgreSQL está funcionando
python setup_postgres.py status
```

### 2. Configuração Automática
```bash
# Script automatizado de configuração
python setup_postgres.py
```

### 3. Configuração Manual

#### Passo 1: Criar usuário e banco
```sql
-- Conectar como superusuário
psql -U postgres

-- Criar usuário (opcional)
CREATE USER veterinaria_user WITH PASSWORD 'sua_senha_segura';

-- Criar banco de dados
CREATE DATABASE veterinaria_db OWNER veterinaria_user;

-- Dar permissões
GRANT ALL PRIVILEGES ON DATABASE veterinaria_db TO veterinaria_user;
```

#### Passo 2: Configurar .env
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
ENVIRONMENT=production
DATABASE_URL=postgresql://veterinaria_user:sua_senha_segura@localhost:5432/veterinaria_db

# Ou usar configurações separadas
POSTGRES_USER=veterinaria_user
POSTGRES_PASSWORD=sua_senha_segura
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=veterinaria_db
```

#### Passo 3: Inicializar banco
```bash
# Criar tabelas
python init_db.py

# Popular com dados de exemplo (opcional)
python populate_db.py
```

## 🚀 Execução

```bash
# Executar servidor
python -m uvicorn main:app --reload

# Ou com configurações específicas
ENVIRONMENT=production python -m uvicorn main:app --reload
```

## 🔍 Verificação

### Testar Conexão
```bash
# Via script Python
python -c "from database import engine; print('✅ Conexão OK' if engine.connect() else '❌ Erro')"

# Via psql
psql -U veterinaria_user -d veterinaria_db -c "SELECT version();"
```

### Verificar Tabelas
```sql
-- Conectar ao banco
psql -U veterinaria_user -d veterinaria_db

-- Listar tabelas
\dt

-- Ver estrutura de uma tabela
\d clinicas
```

## 🛠️ Solução de Problemas

### Erro: "peer authentication failed"
```bash
# Editar pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Trocar "peer" por "md5" para local connections
local   all             all                                     md5
```

### Erro: "could not connect to server"
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql  # Linux
brew services list | grep postgres  # macOS
services.msc  # Windows (procurar por postgresql)

# Iniciar serviço
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

### Erro: "database does not exist"
```sql
-- Conectar como superusuário e criar banco
psql -U postgres
CREATE DATABASE veterinaria_db;
```

### Erro: "password authentication failed"
```bash
# Resetar senha do postgres
sudo -u postgres psql
ALTER USER postgres PASSWORD 'nova_senha';
```

## 📊 Comandos Úteis

### Backup
```bash
# Backup do banco
pg_dump -U veterinaria_user veterinaria_db > backup.sql

# Restore
psql -U veterinaria_user veterinaria_db < backup.sql
```

### Monitoramento
```sql
-- Ver conexões ativas
SELECT * FROM pg_stat_activity WHERE datname = 'veterinaria_db';

-- Ver tamanho das tabelas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public';
```

## 🔄 Migração SQLite → PostgreSQL

```bash
# 1. Fazer backup dos dados SQLite
python backup_sqlite.py

# 2. Configurar PostgreSQL
python setup_postgres.py

# 3. Migrar dados
python migrate_sqlite_to_postgres.py

# 4. Atualizar .env
ENVIRONMENT=production
DATABASE_URL=postgresql://...
```

## 📝 Notas Importantes

1. **Segurança**: Use senhas fortes em produção
2. **Performance**: Configure `shared_buffers`, `effective_cache_size`
3. **Backup**: Configure backup automático
4. **SSL**: Use SSL em produção (`sslmode=require`)
5. **Firewall**: Configure adequadamente para produção

## 🌐 Configuração para Deploy

### Docker Compose
```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: veterinaria_db
      POSTGRES_USER: veterinaria_user
      POSTGRES_PASSWORD: senha_segura
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Heroku
```bash
# Adicionar addon PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Ver configurações
heroku config
```

### AWS RDS
- Use o endpoint fornecido pela AWS
- Configure security groups adequadamente
- Use SSL/TLS em produção
