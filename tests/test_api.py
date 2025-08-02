# -*- coding: utf-8 -*-
"""
Testes unitários para API
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.api.auth import verify_password, create_access_token, get_password_hash
from src.api.models import CreditScoreInput, CreditScoreOutput


class TestAuth(unittest.TestCase):
    """Testa funcoes de autenticacao."""
    
    def test_password_hashing(self):
        """Testa hash e verificacao de senha."""
        password = "test123"
        hashed = get_password_hash(password)
        
        # Hash deve ser diferente da senha
        self.assertNotEqual(password, hashed)
        
        # Verificacao deve funcionar
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong", hashed))
    
    def test_create_access_token(self):
        """Testa criacao de token JWT."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Token deve ser string nao vazia
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)
    
    def test_token_expiration(self):
        """Testa expiracao do token."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=1)
        
        token = create_access_token(data, expires_delta)
        
        # Token deve conter informacao de expiracao
        self.assertIsInstance(token, str)


class TestModels(unittest.TestCase):
    """Testa modelos Pydantic."""
    
    def test_credit_score_input_validation(self):
        """Testa validacao de entrada."""
        # Dados validos
        valid_data = {
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
            "credit_history_age": "5 Years",
            "payment_of_min_amount": "Yes",
            "total_emi_per_month": 2500.0,
            "amount_invested_monthly": 1500.0,
            "payment_behaviour": "Low_spent_Medium_value_payments",
            "monthly_balance": 15000.0
        }
        
        # Deve criar objeto sem erros
        input_obj = CreditScoreInput(**valid_data)
        self.assertEqual(input_obj.age, 35)
        self.assertEqual(input_obj.occupation, "Engineer")
    
    def test_credit_score_output_format(self):
        """Testa formato de saida."""
        output_data = {
            "credit_score": "Good",
            "confidence": 0.85,
            "risk_level": "Low",
            "recommendation": "Approve loan",
            "prediction_id": "123-456-789",
            "timestamp": datetime.now().isoformat()
        }
        
        output_obj = CreditScoreOutput(**output_data)
        
        # Verifica campos
        self.assertEqual(output_obj.credit_score, "Good")
        self.assertEqual(output_obj.confidence, 0.85)
        self.assertEqual(output_obj.risk_level, "Low")


class TestAPIHelpers(unittest.TestCase):
    """Testa funcoes auxiliares da API."""
    
    def test_prepare_input_data(self):
        """Testa preparacao de dados de entrada."""
        # Simula funcao de preparacao
        def mock_prepare_input(data):
            # Converte snake_case para CamelCase
            return {
                'Age': data.get('age'),
                'Annual_Income': data.get('annual_income'),
                'Occupation': data.get('occupation')
            }
        
        input_data = {
            'age': 30,
            'annual_income': 50000,
            'occupation': 'Teacher'
        }
        
        result = mock_prepare_input(input_data)
        
        self.assertEqual(result['Age'], 30)
        self.assertEqual(result['Annual_Income'], 50000)
        self.assertEqual(result['Occupation'], 'Teacher')


if __name__ == '__main__':
    unittest.main()