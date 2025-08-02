"""
Arquivo de configuração central do projeto QuantumFinance
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025

Centraliza todas as configurações e constantes do projeto.
"""

from pathlib import Path

# Caminhos do projeto
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_PROCESSED = DATA_DIR / "processed"
DATA_FINAL = DATA_DIR / "final"
MODELS_DIR = PROJECT_ROOT / "models"

# Configurações do modelo
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Configurações MLflow
MLFLOW_TRACKING_URI = f"file:///{PROJECT_ROOT}/mlruns"
MLFLOW_EXPERIMENT_NAME = "credit-score-classification"

# Configurações da API
API_VERSION = "v1"
API_TITLE = "QuantumFinance Credit Score API"
API_DESCRIPTION = "API para classificação de score de crédito"

# Configurações de autenticação
SECRET_KEY = "seu-secret-key-aqui-mudar-em-producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30