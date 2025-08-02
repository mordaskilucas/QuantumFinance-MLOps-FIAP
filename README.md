# QuantumFinance - Sistema de Score de Crédito

## Descrição do Projeto
Sistema de classificação de score de crédito desenvolvido pela QuantumFinance em parceria com empresas clientes. O objetivo é fornecer um modelo simples e eficiente para avaliar o score de crédito baseado em transações recentes dos clientes.

## Objetivos
- Treinar um modelo de classificação de score de crédito
- Implementar rastreamento de experimentos com MLflow
- Criar API REST segura com autenticação JWT
- Desenvolver interface Streamlit para demonstração
- Garantir governança e versionamento do modelo

## Estrutura do Projeto
```
QuantumFinance/
├── data/
│   ├── raw/              # Dados originais do Kaggle
│   ├── processed/        # Dados processados
│   └── final/           # Dados prontos para modelagem
├── models/              # Modelos treinados
├── notebooks/           # Notebooks de análise e modelagem
├── src/                 # Código fonte
│   ├── api/            # API FastAPI
│   ├── features/       # Engenharia de features
│   └── modeling/       # Scripts de treinamento
├── reports/            # Relatórios e visualizações
├── tests/              # Testes unitários
└── app/               # Aplicação Streamlit
```

## Instalação e Configuração

Para instruções detalhadas de instalação, consulte o arquivo [INSTALACAO.md](INSTALACAO.md).

### Instalação Rápida
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd QuantumFinance

# Crie ambiente virtual e instale dependências
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Execute o sistema
python run_app.py
```

## Uso do Sistema

### API REST
- Documentação: http://localhost:8000/docs
- Endpoints principais:
  - POST `/token` - Autenticação
  - POST `/predict` - Predição individual
  - POST `/predict/batch` - Predição em lote
  - GET `/health` - Status da API

### Interface Streamlit
- Acesso: http://localhost:8501
- Funcionalidades:
  - Login com credenciais
  - Análise individual de score
  - Análise em lote via CSV
  - Download de resultados

### Credenciais de Acesso
- **Usuário**: admin | **Senha**: quantumfinance123
- **Usuário**: analista | **Senha**: quantumfinance123

## Tecnologias Utilizadas
- Python 3.9
- Pandas & NumPy (análise de dados)
- Scikit-learn (modelagem)
- MLflow (rastreamento de experimentos)
- FastAPI (API REST)
- Streamlit (interface web)
- Docker (containerização)

## Comandos Úteis (Makefile)

```bash
make install    # Instalar dependências
make data       # Processar dados
make train      # Treinar modelo
make api        # Iniciar API
make app        # Iniciar Streamlit
make run        # Iniciar sistema completo
make mlflow     # Abrir MLflow UI
make clean      # Limpar arquivos temporários
```

## Autores
- 357103 - Víctor Kennedy Kaneko Nunes
- 358078 - Octavio Ribeiro
- 360075 - Gabriel Oliveira
- 358032 - Lucas Guilherme Mordaski

Trabalho de MLOps - MBA FIAP