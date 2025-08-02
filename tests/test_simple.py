# -*- coding: utf-8 -*-
"""
Teste simples para verificar funcionamento básico
"""

import unittest
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestSimple(unittest.TestCase):
    """Testes simples de verificação."""
    
    def test_imports(self):
        """Testa se os módulos podem ser importados."""
        try:
            from src.features import prepare_data
            from src.api import main
            from src.api import auth
            from src.api import models
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Erro ao importar módulo: {e}")
    
    def test_basic_math(self):
        """Teste básico de matemática."""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(10 * 5, 50)
        self.assertTrue(100 > 50)
    
    def test_string_operations(self):
        """Teste de operações com strings."""
        text = "QuantumFinance"
        self.assertEqual(len(text), 14)
        self.assertTrue(text.startswith("Quantum"))
        self.assertTrue(text.endswith("Finance"))
    
    def test_list_operations(self):
        """Teste de operações com listas."""
        scores = ['Good', 'Standard', 'Poor']
        self.assertEqual(len(scores), 3)
        self.assertIn('Good', scores)
        self.assertNotIn('Excellent', scores)


if __name__ == '__main__':
    unittest.main()