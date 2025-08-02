# Instruções de Entrega - QuantumFinance

## Checklist de Requisitos Implementados

### 1. Template de Repositório ✅
- Estrutura organizada seguindo Cookiecutter Data Science
- Separação clara entre dados, modelos, código fonte e aplicação

### 2. Rastreamento de Experimentos ✅
- MLflow configurado para tracking de experimentos
- Comparação entre modelos (Logistic Regression vs Random Forest)
- Métricas registradas: accuracy, precision, recall, f1_score
- Feature importance do modelo vencedor

### 3. Versionamento do Modelo ✅
- Model Registry do MLflow implementado
- Múltiplas versões do modelo `credit_score_classifier`
- Modelos salvos com timestamp em `models/`

### 4. API Segura ✅
- **Autenticação**: JWT Token implementado
- **Rate Limiting**: 10 req/min (individual), 2 req/min (batch)
- **Endpoints**:
  - POST /token - Autenticação
  - POST /predict - Predição individual
  - POST /predict/batch - Predição em lote
  - GET /health - Status da API

### 5. Documentação da API ✅
- Swagger UI disponível em http://localhost:8000/docs
- ReDoc disponível em http://localhost:8000/redoc
- Arquivo API_README.md com exemplos detalhados

### 6. Aplicação Streamlit ✅
- Interface completa integrada com a API
- Login com autenticação JWT
- Análise individual e em lote
- Download de resultados em CSV

## Como Executar

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Processar dados** (se necessário):
   ```bash
   python src/features/prepare_data.py
   ```

3. **Treinar modelo** (se necessário):
   ```bash
   python src/modeling/train_model.py
   ```

4. **Executar sistema completo**:
   ```bash
   python run_app.py
   ```

## Observações Importantes

- Dataset do Kaggle já incluído em `data/raw/`
- Modelo já treinado e salvo em `models/`
- Experimentos MLflow em `mlruns/`
- Testado com Python 3.13 no Windows

## Credenciais

- **Usuário**: admin | **Senha**: quantumfinance123
- **Usuário**: analista | **Senha**: quantumfinance123

## Estrutura de Arquivos

```
QuantumFinance/
├── data/               # Dados (raw, processed, final)
├── models/             # Modelos treinados
├── mlruns/             # Experimentos MLflow
├── src/                # Código fonte
│   ├── api/           # API REST (FastAPI)
│   ├── features/      # Preparação de dados
│   └── modeling/      # Treinamento
├── app/               # Aplicação Streamlit
├── notebooks/         # Análise exploratória
└── run_app.py        # Script principal
```

## Autores

- 357103 - Víctor Kennedy Kaneko Nunes
- 358078 - Octavio Ribeiro
- 360075 - Gabriel Oliveira
- 358032 - Lucas Guilherme Mordaski

Trabalho de MLOps - MBA FIAP