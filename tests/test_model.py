# -*- coding: utf-8 -*-
"""
Testes unitários para modelo de ML
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestModelTraining(unittest.TestCase):
    """Testa treinamento e validacao do modelo."""
    
    def setUp(self):
        """Prepara dados de teste."""
        np.random.seed(42)
        
        # Cria dataset sintético
        self.n_samples = 1000
        self.X = pd.DataFrame({
            'Age': np.random.randint(18, 70, self.n_samples),
            'Annual_Income': np.random.uniform(20000, 200000, self.n_samples),
            'Num_Bank_Accounts': np.random.randint(1, 5, self.n_samples),
            'Num_Credit_Card': np.random.randint(0, 6, self.n_samples),
            'Outstanding_Debt': np.random.uniform(0, 100000, self.n_samples),
            'Credit_Utilization_Ratio': np.random.uniform(0, 100, self.n_samples),
            'Payment_Score': np.random.uniform(0, 100, self.n_samples)
        })
        
        # Cria target baseado em regras simples
        self.y = pd.Series(
            np.where(
                (self.X['Payment_Score'] > 70) & (self.X['Credit_Utilization_Ratio'] < 30),
                'Good',
                np.where(
                    (self.X['Payment_Score'] < 40) | (self.X['Credit_Utilization_Ratio'] > 80),
                    'Poor',
                    'Standard'
                )
            )
        )
    
    def test_data_split(self):
        """Testa divisao treino/teste."""
        from sklearn.model_selection import train_test_split
        
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Verifica tamanhos
        self.assertEqual(len(X_train), 800)
        self.assertEqual(len(X_test), 200)
        self.assertEqual(len(y_train), 800)
        self.assertEqual(len(y_test), 200)
    
    def test_model_predictions(self):
        """Testa predicoes do modelo."""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Treina modelo simples
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Faz predicoes
        predictions = model.predict(X_test)
        
        # Verifica formato das predicoes
        self.assertEqual(len(predictions), len(X_test))
        self.assertTrue(all(pred in ['Good', 'Standard', 'Poor'] for pred in predictions))
    
    def test_model_probabilities(self):
        """Testa probabilidades do modelo."""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Obtem probabilidades
        proba = model.predict_proba(X_test)
        
        # Verifica formato
        self.assertEqual(proba.shape[0], len(X_test))
        self.assertEqual(proba.shape[1], 3)  # 3 classes
        
        # Soma das probabilidades deve ser 1
        for row in proba:
            self.assertAlmostEqual(sum(row), 1.0, places=5)
    
    def test_feature_importance(self):
        """Testa importancia das features."""
        from sklearn.ensemble import RandomForestClassifier
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(self.X, self.y)
        
        # Obtem importancias
        importances = model.feature_importances_
        
        # Verifica formato
        self.assertEqual(len(importances), len(self.X.columns))
        
        # Todas importancias devem ser >= 0
        self.assertTrue(all(imp >= 0 for imp in importances))
        
        # Soma deve ser aproximadamente 1
        self.assertAlmostEqual(sum(importances), 1.0, places=5)


class TestModelValidation(unittest.TestCase):
    """Testa validacao e metricas do modelo."""
    
    def test_accuracy_calculation(self):
        """Testa calculo de acuracia."""
        from sklearn.metrics import accuracy_score
        
        y_true = ['Good', 'Good', 'Poor', 'Standard', 'Good']
        y_pred = ['Good', 'Good', 'Poor', 'Standard', 'Poor']
        
        accuracy = accuracy_score(y_true, y_pred)
        
        # 4 de 5 corretos = 0.8
        self.assertEqual(accuracy, 0.8)
    
    def test_confusion_matrix(self):
        """Testa matriz de confusao."""
        from sklearn.metrics import confusion_matrix
        
        y_true = ['Good', 'Good', 'Poor', 'Poor']
        y_pred = ['Good', 'Poor', 'Poor', 'Good']
        
        cm = confusion_matrix(y_true, y_pred, labels=['Good', 'Poor'])
        
        # Verifica formato
        self.assertEqual(cm.shape, (2, 2))
        
        # Verifica valores
        self.assertEqual(cm[0, 0], 1)  # Good previsto como Good
        self.assertEqual(cm[0, 1], 1)  # Good previsto como Poor
        self.assertEqual(cm[1, 0], 1)  # Poor previsto como Good
        self.assertEqual(cm[1, 1], 1)  # Poor previsto como Poor


if __name__ == '__main__':
    unittest.main()