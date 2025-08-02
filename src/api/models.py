# -*- coding: utf-8 -*-
"""
Modelos Pydantic para a API
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025

Define os schemas de entrada e saida da API.
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Modelo de entrada para predicao
class CreditScoreInput(BaseModel):
    """Dados de entrada para predicao de score de credito."""
    
    # Informacoes pessoais
    age: int = Field(..., ge=18, le=100, description="Idade do cliente")
    occupation: str = Field(..., description="Ocupacao do cliente")
    
    # Informacoes financeiras
    annual_income: float = Field(..., gt=0, description="Renda anual")
    monthly_inhand_salary: float = Field(..., gt=0, description="Salario mensal liquido")
    num_bank_accounts: int = Field(..., ge=0, description="Numero de contas bancarias")
    num_credit_card: int = Field(..., ge=0, description="Numero de cartoes de credito")
    interest_rate: float = Field(..., ge=0, le=100, description="Taxa de juros")
    num_of_loan: int = Field(..., ge=0, description="Numero de emprestimos")
    
    # Tipos de emprestimo
    type_of_loan: str = Field(..., description="Tipos de emprestimo")
    
    # Historico de pagamento
    delay_from_due_date: int = Field(..., description="Dias de atraso desde o vencimento")
    num_of_delayed_payment: int = Field(..., ge=0, description="Numero de pagamentos atrasados")
    changed_credit_limit: float = Field(..., description="Mudanca no limite de credito")
    num_credit_inquiries: int = Field(..., ge=0, description="Numero de consultas de credito")
    
    # Mix de credito e dividas
    credit_mix: str = Field(..., description="Mix de credito")
    outstanding_debt: float = Field(..., ge=0, description="Divida pendente")
    credit_utilization_ratio: float = Field(..., ge=0, le=100, description="Taxa de utilizacao de credito")
    
    # Historico e comportamento
    credit_history_age: str = Field(..., description="Idade do historico de credito")
    payment_of_min_amount: str = Field(..., description="Pagamento do valor minimo")
    total_emi_per_month: float = Field(..., ge=0, description="Total EMI por mes")
    amount_invested_monthly: float = Field(..., ge=0, description="Valor investido mensalmente")
    payment_behaviour: str = Field(..., description="Comportamento de pagamento")
    monthly_balance: float = Field(..., description="Saldo mensal")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

# Modelo de resposta para predicao
class CreditScoreResponse(BaseModel):
    """Resposta da predicao de score de credito."""
    credit_score: str = Field(..., description="Score de credito previsto (Good, Standard, Poor)")
    confidence: float = Field(..., description="Confianca da predicao (0-1)")
    prediction_id: str = Field(..., description="ID unico da predicao")
    timestamp: datetime = Field(..., description="Timestamp da predicao")
    
    # Detalhes adicionais
    risk_level: str = Field(..., description="Nivel de risco (Low, Medium, High)")
    recommendation: str = Field(..., description="Recomendacao baseada no score")
    
    class Config:
        json_schema_extra = {
            "example": {
                "credit_score": "Good",
                "confidence": 0.85,
                "prediction_id": "pred_123456",
                "timestamp": "2025-01-15T10:30:00",
                "risk_level": "Low",
                "recommendation": "Cliente elegivel para credito com condicoes favoraveis"
            }
        }

# Modelo para status da API
class HealthResponse(BaseModel):
    """Status de saude da API."""
    status: str = Field(..., description="Status da API")
    model_version: str = Field(..., description="Versao do modelo")
    api_version: str = Field(..., description="Versao da API")
    timestamp: datetime = Field(..., description="Timestamp atual")

# Modelo para batch prediction
class BatchCreditScoreInput(BaseModel):
    """Entrada para predicao em lote."""
    predictions: List[CreditScoreInput] = Field(..., description="Lista de clientes para predicao")
    
class BatchCreditScoreResponse(BaseModel):
    """Resposta para predicao em lote."""
    results: List[CreditScoreResponse] = Field(..., description="Lista de resultados")
    total_processed: int = Field(..., description="Total de predicoes processadas")
    processing_time: float = Field(..., description="Tempo de processamento em segundos")