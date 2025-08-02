# QuantumFinance - Sistema de Score de Crédito

Sistema completo de MLOps para classificação de score de crédito desenvolvido para o MBA FIAP.

## Visão Geral

O QuantumFinance é uma solução end-to-end que implementa:
- Análise e preparação de dados
- Treinamento de modelo com MLflow
- API REST segura com FastAPI
- Interface web com Streamlit
- Monitoramento e versionamento de modelos

## Quick Start

### 1. Clonar o Repositório
```bash
git clone <seu-repositorio>
cd QuantumFinance
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Preparar Dados
```bash
# Baixar dataset do Kaggle e colocar em data/raw/
# https://www.kaggle.com/datasets/parisrohan/credit-score-classification

# Processar dados
make data
```

### 4. Treinar Modelo
```bash
make train
```

### 5. Executar Sistema
```bash
make run
```

Isso iniciará:
- API em http://localhost:8000
- Streamlit em http://localhost:8501
- MLflow UI em http://localhost:5000 (executar `make mlflow` separadamente)

## Estrutura do Projeto

```
QuantumFinance/
├── app/                      # Aplicação Streamlit
│   ├── app.py               # Interface principal
│   └── .streamlit/          # Configurações do Streamlit
├── data/                    # Dados do projeto
│   ├── raw/                # Dados originais
│   ├── processed/          # Dados processados
│   └── final/              # Dados prontos para modelagem
├── models/                  # Modelos treinados
├── notebooks/               # Jupyter notebooks
│   └── 01_eda_credit_score.ipynb
├── src/                     # Código fonte
│   ├── api/                # API REST
│   │   ├── main.py        # Endpoints principais
│   │   ├── auth.py        # Autenticação JWT
│   │   └── models.py      # Schemas Pydantic
│   ├── features/           # Processamento de dados
│   │   └── prepare_data.py
│   └── modeling/           # Treinamento
│       └── train_model.py
├── mlruns/                  # Experimentos MLflow
├── config.py               # Configurações centralizadas
├── requirements.txt        # Dependências
├── Makefile               # Comandos automatizados
└── README.md              # Este arquivo
```

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `make install` | Instala todas as dependências |
| `make data` | Processa os dados brutos |
| `make train` | Treina o modelo |
| `make api` | Inicia apenas a API |
| `make app` | Inicia apenas o Streamlit |
| `make run` | Inicia API + Streamlit |
| `make mlflow` | Abre interface do MLflow |
| `make test` | Executa os testes |
| `make clean` | Limpa arquivos temporários |

## Funcionalidades

### 1. Preparação de Dados
- Limpeza e tratamento de valores faltantes
- Engenharia de features
- Normalização e codificação

### 2. Modelo de Machine Learning
- **Algoritmo**: Random Forest
- **Accuracy**: 77.5%
- **Features**: 25 variáveis + 3 engenheiradas
- **Tracking**: MLflow para experimentos

### 3. API REST
- **Framework**: FastAPI
- **Autenticação**: JWT Token
- **Rate Limiting**: 10 req/min (individual), 2 req/min (batch)
- **Documentação**: Swagger UI em `/docs`

### 4. Interface Web
- **Framework**: Streamlit
- **Funcionalidades**:
  - Análise individual
  - Análise em lote (CSV)
  - Download de resultados
  - Visualização de métricas

## Autenticação

### Usuários de Teste
| Username | Password | Role |
|----------|----------|------|
| admin | quantumfinance123 | Administrador |
| analista | quantumfinance123 | Analista |

### Obter Token (API)
```python
import requests

response = requests.post(
    "http://localhost:8000/token",
    data={"username": "admin", "password": "quantumfinance123"}
)
token = response.json()["access_token"]
```

## Exemplo de Uso

### Via Interface Web
1. Acesse http://localhost:8501
2. Faça login com as credenciais
3. Preencha os dados do cliente
4. Clique em "Analisar Score de Crédito"

### Via API
```python
import requests

# Autenticar
token_response = requests.post(
    "http://localhost:8000/token",
    data={"username": "admin", "password": "quantumfinance123"}
)
token = token_response.json()["access_token"]

# Fazer predição
headers = {"Authorization": f"Bearer {token}"}
data = {
    "age": 35,
    "occupation": "Engineer",
    "annual_income": 120000,
    # ... outros campos
}

prediction = requests.post(
    "http://localhost:8000/predict",
    json=data,
    headers=headers
)

print(prediction.json())
```

## Monitoramento

### MLflow
```bash
make mlflow
# Acesse http://localhost:5000
```

Visualize:
- Experimentos
- Métricas
- Parâmetros
- Modelos versionados

## Testes

### Testar API
```bash
python test_api.py
```

### Testes Unitários
```bash
pytest tests/ -v
```

## Troubleshooting

### Erro: Porta em uso
```bash
# Windows - encontrar processo
netstat -ano | findstr :8000
# Matar processo
taskkill /F /PID <PID>
```

### Erro: Modelo não encontrado
```bash
# Retreinar modelo
make train
```

### Erro: Token expirado
- Faça login novamente
- Token expira em 30 minutos

## Tecnologias Utilizadas

- **Python 3.9+**
- **Pandas & NumPy**: Análise de dados
- **Scikit-learn**: Machine Learning
- **MLflow**: Tracking de experimentos
- **FastAPI**: API REST
- **Streamlit**: Interface web
- **JWT**: Autenticação
- **Docker**: Containerização (opcional)

## Conceitos MLOps Implementados

1. **Versionamento de Código**: Git
2. **Versionamento de Dados**: Estrutura organizada
3. **Tracking de Experimentos**: MLflow
4. **Automação**: Makefile
5. **API REST**: Model serving
6. **Autenticação**: Segurança
7. **Rate Limiting**: Controle de uso
8. **Documentação**: Swagger + README
9. **Testes**: Scripts de validação
10. **Interface**: Aplicação web

## Autor

Desenvolvido por:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
 
 Trabalho de MLOps - MBA FIAP

---

**Nota**: Este é um projeto educacional. Em produção, considere:
- Usar banco de dados para usuários
- Implementar HTTPS
- Adicionar mais testes
- Configurar CI/CD
- Implementar monitoramento em tempo real