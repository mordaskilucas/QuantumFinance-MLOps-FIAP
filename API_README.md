# API QuantumFinance - Score de Crédito

## Visão Geral

API REST desenvolvida com FastAPI para predição de score de crédito usando Machine Learning.

### Recursos Principais:
- Autenticação JWT
- Rate Limiting (throttling)
- Predição individual e em lote
- Documentação interativa (Swagger)
- Rastreamento com MLflow

## Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Treinar Modelo (se necessário)
```bash
python src/modeling/train_model.py
```

### 3. Iniciar API
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Acessar Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Autenticação

### Usuários de Teste
| Username | Password | Role |
|----------|----------|------|
| admin | quantumfinance123 | Administrador |
| analista | quantumfinance123 | Analista |

### Obter Token
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=quantumfinance123"
```

## Endpoints

### 1. Health Check
```
GET /health
```
Retorna status da API e versão do modelo.

### 2. Autenticação
```
POST /token
```
Retorna token JWT para acesso aos endpoints protegidos.

### 3. Predição Individual
```
POST /predict
```
Requer autenticação. Rate limit: 10/minuto.

**Request Body:**
```json
{
  "age": 35,
  "occupation": "Engineer",
  "annual_income": 120000.0,
  "monthly_inhand_salary": 8500.0,
  "num_bank_accounts": 3,
  "num_credit_card": 2,
  "interest_rate": 12.5,
  "num_of_loan": 2,
  "type_of_loan": "Auto Loan, Personal Loan",
  "delay_from_due_date": 5,
  "num_of_delayed_payment": 1,
  "changed_credit_limit": 5.0,
  "num_credit_inquiries": 2,
  "credit_mix": "Good",
  "outstanding_debt": 25000.0,
  "credit_utilization_ratio": 35.5,
  "credit_history_age": "5 Years and 2 Months",
  "payment_of_min_amount": "Yes",
  "total_emi_per_month": 2500.0,
  "amount_invested_monthly": 1500.0,
  "payment_behaviour": "Low_spent_Medium_value_payments",
  "monthly_balance": 15000.0
}
```

**Response:**
```json
{
  "credit_score": "Good",
  "confidence": 0.85,
  "prediction_id": "pred_123456",
  "timestamp": "2025-01-15T10:30:00",
  "risk_level": "Low",
  "recommendation": "Cliente elegível para crédito com condições favoráveis"
}
```

### 4. Predição em Lote
```
POST /predict/batch
```
Requer autenticação. Rate limit: 2/minuto. Máximo 100 clientes por requisição.

### 5. Informações do Usuário
```
GET /users/me
```
Retorna informações do usuário autenticado.

## 🛡️ Rate Limiting

| Endpoint | Limite |
|----------|--------|
| /predict | 10 requisições/minuto |
| /predict/batch | 2 requisições/minuto |

## Modelo

### Features Utilizadas (25 total)
- **Informações Pessoais**: age, occupation
- **Financeiras**: annual_income, monthly_inhand_salary, etc.
- **Histórico**: credit_history_age, payment_behaviour
- **Features Engenheiradas**: Debt_Income_Ratio, Total_Credit_Usage, Payment_Score

### Performance
- **Accuracy**: 77.5%
- **F1-Score**: 77.5%
- **Modelo**: Random Forest

## 🧪 Testar API

Use o script de teste fornecido:
```bash
python test_api.py
```

Ou teste manualmente com curl:

```bash
# 1. Obter token
TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=quantumfinance123" \
  | jq -r '.access_token')

# 2. Fazer predição
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @exemplo.json
```

## Configuração

Variáveis de ambiente (.env):
```
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=seu-secret-key-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Monitoramento

### MLflow UI
```bash
mlflow ui
```
Acesse: http://localhost:5000

## 🚨 Troubleshooting

### Erro: Modelo não encontrado
```bash
python src/modeling/train_model.py
```

### Erro: Porta em uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### Erro: Token expirado
Faça login novamente para obter novo token.

## 👥 Autor
Aluno MBA FIAP - MLOps