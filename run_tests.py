# -*- coding: utf-8 -*-
"""
Script para executar todos os testes
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
"""

import unittest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Executa todos os testes do projeto."""
    # Descobre todos os testes
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retorna 0 se todos passaram, 1 caso contrário
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("\n" + "="*60)
    print("EXECUTANDO TESTES UNITÁRIOS - QUANTUMFINANCE")
    print("="*60 + "\n")
    
    exit_code = run_all_tests()
    
    print("\n" + "="*60)
    if exit_code == 0:
        print("TODOS OS TESTES PASSARAM!")
    else:
        print("ALGUNS TESTES FALHARAM!")
    print("="*60 + "\n")
    
    sys.exit(exit_code)