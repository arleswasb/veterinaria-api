# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instala o cliente do PostgreSQL para que o entrypoint possa verificar a conexão
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o diretório de trabalho
COPY . .

# Torna o script de entrypoint executável
RUN chmod +x ./entrypoint.sh

# Expõe a porta que a aplicação irá rodar
EXPOSE 8000