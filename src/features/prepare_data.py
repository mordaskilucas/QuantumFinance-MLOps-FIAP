# -*- coding: utf-8 -*-
"""
Script de preparação de dados para o modelo de Score de Crédito
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import json
warnings.filterwarnings('ignore')

# Importar configurações do projeto
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import DATA_RAW, DATA_PROCESSED, DATA_FINAL

# Criar pastas se não existirem
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
DATA_FINAL.mkdir(parents=True, exist_ok=True)

def load_and_explore():
    """Carrega e explora os dados iniciais."""
    print("Carregando dados brutos...")
    
    # Carregar train.csv
    df = pd.read_csv(DATA_RAW / "train.csv")
    print(f"Dados carregados: {df.shape[0]} linhas e {df.shape[1]} colunas")
    
    # Mostrar informações básicas
    print("\nPrimeiras linhas do dataset:")
    print(df.head())
    
    print("\nInformacoes sobre as colunas:")
    print(df.info())
    
    print("\nDistribuicao do target (Credit_Score):")
    print(df['Credit_Score'].value_counts())
    
    return df

def clean_numeric_columns(df):
    """Limpa e converte colunas numéricas."""
    print("\nLimpando colunas numericas...")
    
    # Lista de colunas que deveriam ser numéricas
    numeric_cols = ['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 
                    'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate',
                    'Num_of_Loan', 'Outstanding_Debt', 'Credit_Utilization_Ratio',
                    'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance',
                    'Num_of_Delayed_Payment', 'Num_Credit_Inquiries']
    
    for col in numeric_cols:
        if col in df.columns:
            # Converter para string primeiro para limpar
            df[col] = df[col].astype(str)
            
            # Remover caracteres especiais
            df[col] = df[col].str.replace('_', '')
            df[col] = df[col].str.replace(',', '')
            
            # Converter para numérico, erros viram NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Preencher NaN com mediana
            if df[col].isnull().sum() > 0:
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
                print(f"   - {col}: valores faltantes preenchidos com mediana ({median_value:.2f})")
    
    return df

def clean_categorical_columns(df):
    """Limpa colunas categóricas."""
    print("\nLimpando colunas categoricas...")
    
    # Preencher valores faltantes em colunas de texto
    text_cols = df.select_dtypes(include=['object']).columns
    
    for col in text_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna('Unknown', inplace=True)
            print(f"   - {col}: valores faltantes preenchidos com 'Unknown'")
    
    return df

def create_features(df):
    """Cria novas features de forma segura."""
    print("\nCriando novas features...")
    
    # 1. Ratio Dívida/Renda (com tratamento de erros)
    if 'Outstanding_Debt' in df.columns and 'Annual_Income' in df.columns:
        # Garantir que são numéricas
        df['Debt_Income_Ratio'] = df['Outstanding_Debt'] / (df['Annual_Income'].replace(0, 1))
        print("   - Criada: Debt_Income_Ratio")
    
    # 2. Utilização total de crédito
    if 'Num_Credit_Card' in df.columns and 'Credit_Utilization_Ratio' in df.columns:
        df['Total_Credit_Usage'] = df['Num_Credit_Card'] * df['Credit_Utilization_Ratio']
        print("   - Criada: Total_Credit_Usage")
    
    # 3. Score de pagamento (baseado em atrasos)
    if 'Num_of_Delayed_Payment' in df.columns:
        df['Payment_Score'] = 100 - (df['Num_of_Delayed_Payment'] * 5)
        df['Payment_Score'] = df['Payment_Score'].clip(0, 100)
        print("   - Criada: Payment_Score")
    
    return df

def prepare_final_dataset(df):
    """Prepara dataset final removendo colunas desnecessárias."""
    print("\nPreparando dataset final...")
    
    # Colunas para remover (identificadores e informações sensíveis)
    cols_to_drop = ['ID', 'Customer_ID', 'Name', 'SSN', 'Month']
    cols_to_drop = [col for col in cols_to_drop if col in df.columns]
    
    df_final = df.drop(columns=cols_to_drop)
    print(f"   - Removidas colunas: {cols_to_drop}")
    
    # Reorganizar com target no final
    if 'Credit_Score' in df_final.columns:
        cols = [col for col in df_final.columns if col != 'Credit_Score']
        cols.append('Credit_Score')
        df_final = df_final[cols]
    
    print(f"Dataset final: {df_final.shape[0]} linhas e {df_final.shape[1]} colunas")
    
    return df_final

def save_data(df_processed, df_final):
    """Salva os dados processados."""
    print("\nSalvando dados...")
    
    # Salvar processado
    df_processed.to_csv(DATA_PROCESSED / "credit_score_processed.csv", index=False)
    print("   - Dados processados salvos")
    
    # Salvar final
    df_final.to_csv(DATA_FINAL / "credit_score_final.csv", index=False)
    print("   - Dados finais salvos")
    
    # Salvar resumo
    summary = {
        'total_linhas': len(df_final),
        'total_colunas': len(df_final.columns),
        'features': list(df_final.columns),
        'distribuicao_target': df_final['Credit_Score'].value_counts().to_dict()
    }
    
    with open(DATA_PROCESSED / "data_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print("   - Resumo salvo")

def main():
    """Pipeline principal."""
    print("\n" + "="*60)
    print("PREPARACAO DE DADOS - QUANTUMFINANCE CREDIT SCORE")
    print("="*60)
    
    # 1. Carregar e explorar
    df = load_and_explore()
    
    # 2. Limpar dados numéricos
    df = clean_numeric_columns(df)
    
    # 3. Limpar dados categóricos
    df = clean_categorical_columns(df)
    
    # 4. Criar features
    df_processed = create_features(df)
    
    # 5. Preparar dataset final
    df_final = prepare_final_dataset(df_processed)
    
    # 6. Salvar
    save_data(df_processed, df_final)
    
    print("\nPROCESSAMENTO CONCLUIDO COM SUCESSO!")
    print("   Proximos passos:")
    print("   1. Executar notebook de EDA")
    print("   2. Treinar modelo com MLflow")
    print("="*60)

if __name__ == "__main__":
    main()