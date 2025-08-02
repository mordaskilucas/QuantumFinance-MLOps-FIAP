# -*- coding: utf-8 -*-
"""
API REST principal para predicao de Score de Credito
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025

API desenvolvida com FastAPI incluindo autenticacao JWT e rate limiting.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from datetime import datetime, timedelta
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import uuid
import time
from typing import List

# Importar modulos locais
import sys
# Adicionar diretorio raiz e diretorio api ao path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent))
from config import API_VERSION, API_TITLE, API_DESCRIPTION, MODELS_DIR, ACCESS_TOKEN_EXPIRE_MINUTES
from models import (
    CreditScoreInput, CreditScoreResponse, 
    HealthResponse,
    BatchCreditScoreInput, BatchCreditScoreResponse
)
from auth import (
    Token, User, authenticate_user, create_access_token,
    get_current_active_user, fake_users_db
)

# Criar aplicacao FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em producao, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Variaveis globais para modelo
MODEL = None
ENCODERS = None
MODEL_VERSION = "1.0.0"

def load_model():
    """Carrega o modelo treinado e encoders."""
    global MODEL, ENCODERS, MODEL_VERSION
    
    print(">> Carregando modelo...")
    
    # Procurar modelo mais recente
    model_dirs = list(MODELS_DIR.glob("random_forest_*"))
    if not model_dirs:
        raise Exception("Nenhum modelo encontrado!")
    
    # Usar o mais recente
    latest_model_dir = sorted(model_dirs)[-1]
    
    # Carregar modelo
    model_path = latest_model_dir / "model.pkl"
    MODEL = joblib.load(model_path)
    
    # Carregar encoders
    encoders_path = latest_model_dir / "encoders.pkl"
    ENCODERS = joblib.load(encoders_path)
    
    MODEL_VERSION = latest_model_dir.name.split("_")[-1]
    print(f">> Modelo carregado: {latest_model_dir.name}")

# Carregar modelo ao iniciar
@app.on_event("startup")
async def startup_event():
    """Evento de inicializacao da API."""
    load_model()
    print(">> API iniciada com sucesso!")

# Endpoint de autenticacao
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login para obter token JWT.
    
    Usuarios de teste:
    - username: admin, password: quantumfinance123
    - username: analista, password: quantumfinance123
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint de health check
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica status da API."""
    return HealthResponse(
        status="healthy",
        model_version=MODEL_VERSION,
        api_version=API_VERSION,
        timestamp=datetime.now()
    )

# Endpoint principal de predicao
@app.post("/predict", response_model=CreditScoreResponse)
@limiter.limit("10/minute")  # Rate limiting: 10 requisicoes por minuto
async def predict_credit_score(
    request: Request,
    credit_input: CreditScoreInput,
    current_user: User = Depends(get_current_active_user)
):
    """
    Prediz o score de credito de um cliente.
    
    Requer autenticacao JWT.
    """
    try:
        # Preparar dados
        input_data = prepare_input_data(credit_input)
        
        # Fazer predicao
        prediction = MODEL.predict(input_data)[0]
        probabilities = MODEL.predict_proba(input_data)[0]
        
        # Decodificar resultado
        credit_score = ENCODERS['target'].inverse_transform([prediction])[0]
        confidence = float(max(probabilities))
        
        # Determinar nivel de risco
        risk_level = get_risk_level(credit_score)
        recommendation = get_recommendation(credit_score)
        
        # Criar resposta
        response = CreditScoreResponse(
            credit_score=credit_score,
            confidence=confidence,
            prediction_id=f"pred_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            risk_level=risk_level,
            recommendation=recommendation
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar predicao: {str(e)}"
        )

# Endpoint de predicao em lote
@app.post("/predict/batch", response_model=BatchCreditScoreResponse)
@limiter.limit("2/minute")  # Rate limiting mais restrito para batch
async def predict_batch(
    request: Request,
    batch_input: BatchCreditScoreInput,
    current_user: User = Depends(get_current_active_user)
):
    """
    Prediz score de credito para multiplos clientes.
    
    Maximo de 100 clientes por requisicao.
    """
    if len(batch_input.predictions) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximo de 100 predicoes por requisicao"
        )
    
    start_time = time.time()
    results = []
    
    for input_item in batch_input.predictions:
        try:
            # Processar cada predicao
            input_data = prepare_input_data(input_item)
            prediction = MODEL.predict(input_data)[0]
            probabilities = MODEL.predict_proba(input_data)[0]
            
            credit_score = ENCODERS['target'].inverse_transform([prediction])[0]
            confidence = float(max(probabilities))
            
            result = CreditScoreResponse(
                credit_score=credit_score,
                confidence=confidence,
                prediction_id=f"pred_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.now(),
                risk_level=get_risk_level(credit_score),
                recommendation=get_recommendation(credit_score)
            )
            results.append(result)
            
        except Exception as e:
            # Em caso de erro, adicionar resultado com erro
            result = CreditScoreResponse(
                credit_score="Error",
                confidence=0.0,
                prediction_id=f"error_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.now(),
                risk_level="Unknown",
                recommendation=f"Erro ao processar: {str(e)}"
            )
            results.append(result)
    
    processing_time = time.time() - start_time
    
    return BatchCreditScoreResponse(
        results=results,
        total_processed=len(results),
        processing_time=processing_time
    )

# Endpoint de informacoes do usuario
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Retorna informacoes do usuario autenticado."""
    return current_user

# Funcoes auxiliares
def prepare_input_data(request: CreditScoreInput) -> pd.DataFrame:
    """Prepara dados de entrada para o modelo."""
    
    # Criar DataFrame com os dados
    data_dict = request.dict()
    
    # Converter nomes das colunas de snake_case para CamelCase
    renamed_dict = {
        'Age': data_dict['age'],
        'Occupation': data_dict['occupation'],
        'Annual_Income': data_dict['annual_income'],
        'Monthly_Inhand_Salary': data_dict['monthly_inhand_salary'],
        'Num_Bank_Accounts': data_dict['num_bank_accounts'],
        'Num_Credit_Card': data_dict['num_credit_card'],
        'Interest_Rate': data_dict['interest_rate'],
        'Num_of_Loan': data_dict['num_of_loan'],
        'Type_of_Loan': data_dict['type_of_loan'],
        'Delay_from_due_date': data_dict['delay_from_due_date'],
        'Num_of_Delayed_Payment': data_dict['num_of_delayed_payment'],
        'Changed_Credit_Limit': data_dict['changed_credit_limit'],
        'Num_Credit_Inquiries': data_dict['num_credit_inquiries'],
        'Credit_Mix': data_dict['credit_mix'],
        'Outstanding_Debt': data_dict['outstanding_debt'],
        'Credit_Utilization_Ratio': data_dict['credit_utilization_ratio'],
        'Credit_History_Age': data_dict['credit_history_age'],
        'Payment_of_Min_Amount': data_dict['payment_of_min_amount'],
        'Total_EMI_per_month': data_dict['total_emi_per_month'],
        'Amount_invested_monthly': data_dict['amount_invested_monthly'],
        'Payment_Behaviour': data_dict['payment_behaviour'],
        'Monthly_Balance': data_dict['monthly_balance']
    }
    
    data = pd.DataFrame([renamed_dict])
    
    # Aplicar mesmas transformacoes do treinamento
    # 1. Codificar categoricas
    categorical_cols = ['Occupation', 'Type_of_Loan', 'Credit_Mix', 
                       'Credit_History_Age', 'Payment_of_Min_Amount', 
                       'Payment_Behaviour']
    
    for col in categorical_cols:
        if col in ENCODERS:
            try:
                data[col] = ENCODERS[col].transform(data[col])
            except:
                # Se valor nao visto, usar o mais comum
                data[col] = 0
    
    # 2. Criar features engenheiradas
    data['Debt_Income_Ratio'] = data['Outstanding_Debt'] / (data['Annual_Income'] + 1)
    data['Total_Credit_Usage'] = data['Num_Credit_Card'] * data['Credit_Utilization_Ratio']
    data['Payment_Score'] = 100 - (data['Num_of_Delayed_Payment'] * 5)
    data['Payment_Score'] = data['Payment_Score'].clip(0, 100)
    
    # 3. Garantir ordem correta das colunas
    expected_features = ['Age', 'Occupation', 'Annual_Income', 'Monthly_Inhand_Salary',
                        'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate',
                        'Num_of_Loan', 'Type_of_Loan', 'Delay_from_due_date',
                        'Num_of_Delayed_Payment', 'Changed_Credit_Limit',
                        'Num_Credit_Inquiries', 'Credit_Mix', 'Outstanding_Debt',
                        'Credit_Utilization_Ratio', 'Credit_History_Age',
                        'Payment_of_Min_Amount', 'Total_EMI_per_month',
                        'Amount_invested_monthly', 'Payment_Behaviour',
                        'Monthly_Balance', 'Debt_Income_Ratio', 'Total_Credit_Usage',
                        'Payment_Score']
    
    data = data[expected_features]
    
    # 4. Padronizar
    data_scaled = ENCODERS['scaler'].transform(data)
    
    return data_scaled

def get_risk_level(credit_score: str) -> str:
    """Determina nivel de risco baseado no score."""
    if credit_score == "Good":
        return "Low"
    elif credit_score == "Standard":
        return "Medium"
    else:
        return "High"

def get_recommendation(credit_score: str) -> str:
    """Gera recomendacao baseada no score."""
    recommendations = {
        "Good": "Cliente elegivel para credito com condicoes favoraveis",
        "Standard": "Cliente elegivel para credito com condicoes padrao",
        "Poor": "Recomenda-se analise adicional antes de aprovar credito"
    }
    return recommendations.get(credit_score, "Score nao reconhecido")

# Endpoint raiz
@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {
        "message": "QuantumFinance Credit Score API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)