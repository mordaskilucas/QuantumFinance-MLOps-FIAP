# Guia de Instalação - QuantumFinance

## Requisitos
- Python 3.8 ou superior (testado com Python 3.13)
- pip
- Windows, Linux ou macOS

## Instalação Rápida

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd QuantumFinance
```

### 2. Crie e ative ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Baixe o dataset
- Acesse: https://www.kaggle.com/datasets/parisrohan/credit-score-classification
- Baixe os arquivos CSV
- Coloque os arquivos na pasta `data/raw/`

## Executar o Sistema

### 1. Processar dados
```bash
python src/features/prepare_data.py
```

### 2. Treinar modelo
```bash
python src/modeling/train_model.py
```

### 3. Iniciar o sistema completo
```bash
python run_app.py
```

Isso iniciará:
- API em http://localhost:8000
- Interface web em http://localhost:8501

## Credenciais de Acesso
- **Usuário**: admin | **Senha**: quantumfinance123
- **Usuário**: analista | **Senha**: quantumfinance123

## Comandos Úteis

Se você tem o Make instalado, pode usar:
```bash
make install    # Instalar dependências
make data       # Processar dados
make train      # Treinar modelo
make run        # Iniciar sistema completo
```

## Solução de Problemas

### Erro de Python
Se aparecer erro de versão do Python, use `py` ao invés de `python`:
```bash
py -m pip install -r requirements.txt
```

### Erro de módulo não encontrado
Certifique-se de que o ambiente virtual está ativado antes de instalar as dependências.

### API não conecta
Verifique se a porta 8000 não está em uso por outro programa.