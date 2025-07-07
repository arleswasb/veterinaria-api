#!/bin/bash

# Aborta o script se qualquer comando falhar
set -e

# Espera o banco de dados PostgreSQL ficar disponível
echo "⏳ Waiting for PostgreSQL to start..."
while ! pg_isready -h db -p 5432 -q -U "$POSTGRES_USER"; do
  sleep 1
done
echo "✅ PostgreSQL started successfully."

# Executa o script para criar e popular o banco de dados
echo "🌱 Initializing and populating the database..."
python populate_db.py

# Inicia o servidor da aplicação FastAPI
echo "🚀 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload