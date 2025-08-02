# -*- coding: utf-8 -*-
"""
Testes unitários para preparação de dados
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.features.prepare_data import create_features, clean_column_names


class TestDataPreparation(unittest.TestCase):
    """Testa funcoes de preparacao de dados."""
    
    def setUp(self):
        """Cria dados de teste."""
        self.test_data = pd.DataFrame({
            'Annual_Income': [50000, 75000, 100000, 30000],
            'Outstanding_Debt': [10000, 20000, 15000, 5000],
            'Monthly_Inhand_Salary': [4000, 6000, 8000, 2500],
            'Num_of_Delayed_Payment': [2, 0, 1, 5],
            'Num_of_Loan': [1, 2, 1, 3],
            'Delay_from_due_date': [5, 0, 2, 15],
            'Payment_of_Min_Amount': ['Yes', 'Yes', 'No', 'No']
        })
    
    def test_create_features(self):
        """Testa criacao de features."""
        result = create_features(self.test_data.copy())
        
        # Verifica se as novas features foram criadas
        self.assertIn('Debt_Income_Ratio', result.columns)
        self.assertIn('Total_Credit_Usage', result.columns)
        self.assertIn('Payment_Score', result.columns)
        
        # Verifica calculos
        expected_ratio = 10000 / 50000
        self.assertAlmostEqual(result.iloc[0]['Debt_Income_Ratio'], expected_ratio, places=4)
    
    def test_clean_column_names(self):
        """Testa limpeza de nomes de colunas."""
        df = pd.DataFrame({
            'Column With Spaces': [1, 2, 3],
            'Column-With-Dashes': [4, 5, 6],
            'UPPERCASE': [7, 8, 9]
        })
        
        result = clean_column_names(df)
        
        # Verifica se os nomes foram limpos
        self.assertIn('column_with_spaces', result.columns)
        self.assertIn('column_with_dashes', result.columns)
        self.assertIn('uppercase', result.columns)
    
    def test_debt_income_ratio_zero_income(self):
        """Testa divisao por zero na razao divida/renda."""
        data = self.test_data.copy()
        data.loc[0, 'Annual_Income'] = 0
        
        result = create_features(data)
        
        # Deve retornar 0 quando income é 0
        self.assertEqual(result.iloc[0]['Debt_Income_Ratio'], 0)
    
    def test_payment_score_calculation(self):
        """Testa calculo do score de pagamento."""
        result = create_features(self.test_data.copy())
        
        # Cliente com poucos atrasos deve ter score alto
        good_client_score = result.iloc[1]['Payment_Score']
        
        # Cliente com muitos atrasos deve ter score baixo
        bad_client_score = result.iloc[3]['Payment_Score']
        
        self.assertGreater(good_client_score, bad_client_score)


if __name__ == '__main__':
    unittest.main()