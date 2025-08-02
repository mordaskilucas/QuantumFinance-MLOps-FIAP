# -*- coding: utf-8 -*-
"""
Script de teste da API
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025

Testa os endpoints da API de Score de Credito.
"""

import requests
import json
from datetime import datetime

# URL base da API
BASE_URL = "http://localhost:8000"

def test_health():
    """Testa endpoint de health."""
    print("\n>> Testando Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_login():
    """Testa autenticacao e obtem token."""
    print("\n>> Testando Login...")
    
    # Dados de login
    login_data = {
        "username": "admin",
        "password": "quantumfinance123"
    }
    
    response = requests.post(
        f"{BASE_URL}/token",
        data=login_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Token obtido com sucesso!")
        return token_data["access_token"]
    else:
        print(f"Erro no login: {response.text}")
        return None

def test_predict(token):
    """Testa predicao de score."""
    print("\n>> Testando Predicao...")
    
    # Dados de exemplo para predicao
    predict_data = {
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
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=predict_data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nResultado da Predicao:")
        print(f"  - Credit Score: {result['credit_score']}")
        print(f"  - Confianca: {result['confidence']:.2%}")
        print(f"  - Nivel de Risco: {result['risk_level']}")
        print(f"  - Recomendacao: {result['recommendation']}")
        print(f"  - ID: {result['prediction_id']}")
    else:
        print(f"Erro na predicao: {response.text}")

def test_batch_predict(token):
    """Testa predicao em lote."""
    print("\n>> Testando Predicao em Lote...")
    
    # Criar 3 clientes de exemplo
    batch_data = {
        "predictions": [
            {
                "age": 25,
                "occupation": "Student",
                "annual_income": 30000.0,
                "monthly_inhand_salary": 2000.0,
                "num_bank_accounts": 1,
                "num_credit_card": 1,
                "interest_rate": 15.0,
                "num_of_loan": 1,
                "type_of_loan": "Student Loan",
                "delay_from_due_date": 10,
                "num_of_delayed_payment": 3,
                "changed_credit_limit": 2.0,
                "num_credit_inquiries": 5,
                "credit_mix": "Standard",
                "outstanding_debt": 15000.0,
                "credit_utilization_ratio": 65.0,
                "credit_history_age": "2 Years",
                "payment_of_min_amount": "No",
                "total_emi_per_month": 800.0,
                "amount_invested_monthly": 200.0,
                "payment_behaviour": "High_spent_Small_value_payments",
                "monthly_balance": 500.0
            },
            {
                "age": 45,
                "occupation": "Manager",
                "annual_income": 200000.0,
                "monthly_inhand_salary": 15000.0,
                "num_bank_accounts": 5,
                "num_credit_card": 4,
                "interest_rate": 8.0,
                "num_of_loan": 3,
                "type_of_loan": "Home Loan, Auto Loan, Personal Loan",
                "delay_from_due_date": 0,
                "num_of_delayed_payment": 0,
                "changed_credit_limit": 10.0,
                "num_credit_inquiries": 1,
                "credit_mix": "Good",
                "outstanding_debt": 50000.0,
                "credit_utilization_ratio": 20.0,
                "credit_history_age": "15 Years",
                "payment_of_min_amount": "Yes",
                "total_emi_per_month": 5000.0,
                "amount_invested_monthly": 5000.0,
                "payment_behaviour": "Low_spent_Large_value_payments",
                "monthly_balance": 50000.0
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json=batch_data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nResultados do Batch:")
        print(f"  - Total processado: {result['total_processed']}")
        print(f"  - Tempo de processamento: {result['processing_time']:.2f}s")
        print(f"\nResultados individuais:")
        for i, pred in enumerate(result['results'], 1):
            print(f"  Cliente {i}: {pred['credit_score']} (confianca: {pred['confidence']:.2%})")
    else:
        print(f"Erro no batch: {response.text}")

def main():
    """Executa todos os testes."""
    print("="*60)
    print("TESTE DA API QUANTUMFINANCE")
    print("="*60)
    
    # 1. Health check
    if not test_health():
        print("\nERRO: API nao esta respondendo!")
        return
    
    # 2. Login
    token = test_login()
    if not token:
        print("\nERRO: Nao foi possivel obter token!")
        return
    
    # 3. Predicao simples
    test_predict(token)
    
    # 4. Predicao em lote
    test_batch_predict(token)
    
    print("\n" + "="*60)
    print("TESTES CONCLUIDOS!")
    print("="*60)

if __name__ == "__main__":
    main()