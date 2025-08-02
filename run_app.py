# -*- coding: utf-8 -*-
"""
Script para iniciar API e Streamlit
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025
"""

import subprocess
import time
import webbrowser
import os
import signal
import sys

def run_api():
    """Inicia a API em background."""
    print("Iniciando API...")
    return subprocess.Popen(
        ["py", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

def run_streamlit():
    """Inicia o Streamlit."""
    print("Iniciando Streamlit...")
    return subprocess.Popen(
        ["py", "-m", "streamlit", "run", "app/app.py", "--server.port", "8501"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

def main():
    """Funcao principal."""
    print("="*60)
    print("QUANTUMFINANCE - SISTEMA DE SCORE DE CREDITO")
    print("="*60)
    
    api_process = None
    streamlit_process = None
    
    try:
        # Iniciar API
        api_process = run_api()
        print("API iniciada em http://localhost:8000")
        print("Documentação em http://localhost:8000/docs")
        
        # Aguardar API iniciar
        time.sleep(3)
        
        # Iniciar Streamlit
        streamlit_process = run_streamlit()
        print("Streamlit iniciado em http://localhost:8501")
        
        # Aguardar um pouco e abrir navegador
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        
        print("\nSistema rodando!")
        print("Pressione Ctrl+C para parar...")
        
        # Manter rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nParando sistema...")
        
        # Parar processos
        if api_process:
            api_process.terminate()
        if streamlit_process:
            streamlit_process.terminate()
            
        print("Sistema parado com sucesso!")
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()