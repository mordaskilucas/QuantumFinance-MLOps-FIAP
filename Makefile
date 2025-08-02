# Makefile para automação do projeto QuantumFinance
# Comandos principais para facilitar o desenvolvimento

.PHONY: help install data train api app test clean run mlflow

# Comando padrão - mostra ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instala todas as dependências"
	@echo "  make data       - Processa os dados brutos"
	@echo "  make train      - Treina o modelo de score de crédito"
	@echo "  make api        - Inicia a API REST"
	@echo "  make app        - Inicia a aplicação Streamlit"
	@echo "  make run        - Inicia API e Streamlit juntos"
	@echo "  make mlflow     - Inicia interface do MLflow"
	@echo "  make test       - Executa os testes"
	@echo "  make clean      - Limpa arquivos temporários"

# Instalar dependências
install:
	pip install -r requirements.txt

# Processar dados
data:
	python src/features/prepare_data.py

# Treinar modelo
train: data
	python src/modeling/train_model.py

# Iniciar API
api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Iniciar aplicação Streamlit
app:
	streamlit run app/app.py

# Executar testes
test:
	python run_tests.py

# Executar sistema completo
run:
	python run_app.py

# Iniciar MLflow UI
mlflow:
	mlflow ui --host 0.0.0.0 --port 5000

# Limpar arquivos temporários
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +