#!/usr/bin/env python3
"""
Script para configurar e testar conexão com PostgreSQL.
Inclui rotina para tentar adicionar o PostgreSQL ao PATH do usuário no Windows.
"""

import subprocess
import sys
import os
import platform  # Importado para lógicas específicas de S.O.
from sqlalchemy import create_engine, text
# Supondo que você tenha um arquivo config.py como nos exemplos anteriores
# from config import settings 

# --- Bloco de Funções de Automação ---

def try_to_fix_windows_path():
    """
    Tenta encontrar a instalação do PostgreSQL no Windows e adicioná-la
    ao PATH do usuário via PowerShell. Retorna True se fizer uma alteração.
    """
    if platform.system() != "Windows":
        return False # Esta função é apenas para Windows

    print("ⓘ  Tentando encontrar e adicionar o PostgreSQL ao PATH do usuário...")

    # Script PowerShell para encontrar o caminho do serviço e adicionar ao PATH do usuário
    powershell_script = r"""
        # Encontra o caminho do executável do serviço PostgreSQL
        $servicePath = (Get-WmiObject -Class Win32_Service -Filter "Name LIKE 'postgresql%'").PathName
        if (-not $servicePath) {
            Write-Output "FAIL: Serviço PostgreSQL não encontrado."
            exit 1
        }

        # Extrai apenas o diretório 'bin' do caminho completo
        $postgresBinPath = [System.IO.Path]::GetDirectoryName($servicePath.Split('"')[1])

        if (-not (Test-Path $postgresBinPath)) {
             Write-Output "FAIL: Diretório bin não encontrado."
             exit 1
        }
        
        # Obtém o PATH atual do usuário
        $currentUserPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

        # Verifica se o caminho já existe no PATH
        if ($currentUserPath -like "*$postgresBinPath*") {
            Write-Output "EXISTS: O caminho já está no PATH do usuário."
            exit 0
        }

        # Adiciona o novo caminho, garantindo que não haja ponto e vírgula no final
        $newPath = $currentUserPath.TrimEnd(';') + ";" + $postgresBinPath
        [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        
        Write-Output "SUCCESS: O caminho foi adicionado ao PATH do usuário."
        exit 0
    """

    try:
        result = subprocess.run(
            ['powershell', '-NoProfile', '-Command', powershell_script],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()

        if "SUCCESS" in output:
            print(f"✅ Sucesso! O caminho '{output.split(':')[-1].strip()}' foi adicionado.")
            return True # Indicamos que uma mudança foi feita
        elif "EXISTS" in output:
            print("👍 O caminho do PostgreSQL já estava no seu PATH. Nenhuma ação necessária.")
            return False # Nenhuma mudança foi feita
        else:
            print(f"❌ A automação falhou em encontrar o caminho. Saída: {output}")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Falha ao executar o script PowerShell de automação: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"   Detalhes do erro: {e.stderr}")
        return False

# --- Bloco de Funções do Script Original ---

def check_postgresql_installation():
    """Verifica se o PostgreSQL está instalado e no PATH."""
    try:
        # Usamos 'psql -V' que é mais padrão que '--version'
        result = subprocess.run(['psql', '-V'], capture_output=True, text=True, check=True)
        print(f"✅ PostgreSQL encontrado: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PostgreSQL não está instalado ou não está no PATH")
        return False

def install_postgresql_windows():
    # ... (Sua função original de instruções manuais)
    pass

def create_database():
    # ... (Sua função original)
    pass

def test_connection():
    # ... (Sua função original)
    pass


# --- Função Principal Modificada ---

def setup_postgresql():
    """Processo completo de configuração do PostgreSQL com automação de PATH."""
    print("🐘 Configuração PostgreSQL para API Veterinária\n")
    
    # 1. Verificar instalação
    if not check_postgresql_installation():
        # Se a verificação falhar, tenta corrigir o PATH automaticamente
        if try_to_fix_windows_path():
            # Se a correção foi aplicada, avisa o usuário e interrompe
            print("\n‼️ AÇÃO NECESSÁRIA ‼️")
            print("O PATH do sistema foi modificado para incluir o PostgreSQL.")
            print("Para que a mudança tenha efeito, você PRECISA FECHAR este terminal e ABRIR UM NOVO.")
            print("\nDepois de reiniciar o terminal, execute este script novamente.")
            sys.exit() # Encerra o script para forçar o reinício do terminal
        else:
            # Se a automação falhou ou não era necessária, mostra instruções manuais
            print("\n⚠️ Automação não pôde resolver o problema. Por favor, configure o PATH manualmente.")
            install_postgresql_windows()
            sys.exit(1) # Encerra com erro

    # ... (o resto do seu script continua aqui)
    print("\n✅ PostgreSQL configurado e pronto para uso!")
    return True


if __name__ == "__main__":
    setup_postgresql()