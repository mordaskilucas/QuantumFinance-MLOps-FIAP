# -*- coding: utf-8 -*-
"""
Script de treinamento do modelo de Score de Crédito com MLflow
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
import joblib
import json
from datetime import datetime

# Bibliotecas de ML
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# MLflow para tracking
import mlflow
import mlflow.sklearn

# Configuracoes
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import DATA_FINAL, MODELS_DIR, MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, RANDOM_STATE, TEST_SIZE

# Criar pasta de modelos
MODELS_DIR.mkdir(exist_ok=True)

# Configurar MLflow
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

def load_data():
    """Carrega dados finais para treinamento."""
    print("Carregando dados finais...")
    
    data_path = DATA_FINAL / "credit_score_final.csv"
    if not data_path.exists():
        print("ERRO: Arquivo de dados finais nao encontrado!")
        return None
    
    df = pd.read_csv(data_path)
    print(f"Dados carregados: {df.shape}")
    
    return df

def prepare_features(df):
    """Prepara features e target para treinamento."""
    print("\nPreparando features...")
    
    # Separar features e target
    X = df.drop(columns=['Credit_Score'])
    y = df['Credit_Score']
    
    # Guardar nomes das features
    feature_names = X.columns.tolist()
    print(f"   - {len(feature_names)} features")
    
    # Dicionario para encoders
    encoders = {}
    
    # 1. Codificar colunas categoricas
    categorical_cols = X.select_dtypes(include=['object']).columns
    print(f"\nCodificando {len(categorical_cols)} colunas categoricas...")
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le
    
    # 2. Codificar target
    print("\nCodificando target...")
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)
    encoders['target'] = target_encoder
    
    print("   Classes:")
    for i, classe in enumerate(target_encoder.classes_):
        print(f"   - {i}: {classe}")
    
    # 3. Padronizar features
    print("\nPadronizando features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    encoders['scaler'] = scaler
    
    return X_scaled, y_encoded, feature_names, encoders

def train_logistic_regression(X_train, y_train, X_test, y_test):
    """Treina Regressao Logistica como baseline."""
    print("\nTreinando Regressao Logistica...")
    
    model = LogisticRegression(
        random_state=RANDOM_STATE,
        max_iter=1000,
        multi_class='multinomial'
    )
    
    # Treinar
    model.fit(X_train, y_train)
    
    # Prever
    y_pred = model.predict(X_test)
    
    # Metricas
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    return model, metrics

def train_random_forest(X_train, y_train, X_test, y_test):
    """Treina Random Forest."""
    print("\nTreinando Random Forest...")
    
    # Modelo com parametros otimizados manualmente
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    
    # Treinar
    model.fit(X_train, y_train)
    
    # Prever
    y_pred = model.predict(X_test)
    
    # Metricas
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    # Feature importance
    feature_importance = model.feature_importances_
    
    return model, metrics, feature_importance

def save_model(model, encoders, model_name, metrics):
    """Salva modelo e componentes."""
    print(f"\nSalvando modelo {model_name}...")
    
    # Criar pasta com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_dir = MODELS_DIR / f"{model_name}_{timestamp}"
    model_dir.mkdir(exist_ok=True)
    
    # Salvar modelo
    joblib.dump(model, model_dir / "model.pkl")
    
    # Salvar encoders
    joblib.dump(encoders, model_dir / "encoders.pkl")
    
    # Salvar metricas
    with open(model_dir / "metrics.json", 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"   - Modelo salvo em: {model_dir}")
    
    return model_dir

def main():
    """Pipeline principal de treinamento."""
    print("\n" + "="*60)
    print("TREINAMENTO DE MODELOS - QUANTUMFINANCE")
    print("="*60)
    
    # 1. Carregar dados
    df = load_data()
    if df is None:
        return
    
    # 2. Preparar features
    X, y, feature_names, encoders = prepare_features(df)
    
    # 3. Dividir dados
    print("\nDividindo dados...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"   - Treino: {X_train.shape[0]} amostras")
    print(f"   - Teste: {X_test.shape[0]} amostras")
    
    # 4. Iniciar experimento MLflow
    print("\nIniciando experimento MLflow...")
    
    with mlflow.start_run(run_name="comparacao_modelos"):
        
        # Log informacoes do dataset
        mlflow.log_param("dataset_size", len(df))
        mlflow.log_param("n_features", len(feature_names))
        mlflow.log_param("test_size", TEST_SIZE)
        
        # 4.1 Treinar Logistic Regression
        print("\n" + "-"*40)
        with mlflow.start_run(run_name="logistic_regression", nested=True):
            lr_model, lr_metrics = train_logistic_regression(X_train, y_train, X_test, y_test)
            
            # Log no MLflow
            mlflow.log_param("model_type", "LogisticRegression")
            mlflow.log_metrics(lr_metrics)
            mlflow.sklearn.log_model(lr_model, "model")
            
            print("\nMetricas Logistic Regression:")
            for metric, value in lr_metrics.items():
                print(f"   - {metric}: {value:.4f}")
        
        # 4.2 Treinar Random Forest
        print("\n" + "-"*40)
        with mlflow.start_run(run_name="random_forest", nested=True):
            rf_model, rf_metrics, feature_imp = train_random_forest(X_train, y_train, X_test, y_test)
            
            # Log no MLflow
            mlflow.log_param("model_type", "RandomForest")
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 20)
            mlflow.log_metrics(rf_metrics)
            mlflow.sklearn.log_model(rf_model, "model")
            
            # Log feature importance
            for i, imp in enumerate(feature_imp[:10]):  # Top 10 features
                mlflow.log_metric(f"feature_imp_{feature_names[i]}", imp)
            
            print("\nMetricas Random Forest:")
            for metric, value in rf_metrics.items():
                print(f"   - {metric}: {value:.4f}")
    
    # 5. Escolher melhor modelo
    print("\n" + "="*40)
    if rf_metrics['f1_score'] > lr_metrics['f1_score']:
        print("MELHOR MODELO: Random Forest")
        best_model = rf_model
        best_metrics = rf_metrics
        model_name = "random_forest"
        
        # Mostrar top features
        print("\nTop 10 Features Importantes:")
        feature_scores = zip(feature_names, feature_imp)
        sorted_features = sorted(feature_scores, key=lambda x: x[1], reverse=True)
        for i, (feat, score) in enumerate(sorted_features[:10]):
            print(f"   {i+1}. {feat}: {score:.4f}")
    else:
        print("MELHOR MODELO: Logistic Regression")
        best_model = lr_model
        best_metrics = lr_metrics
        model_name = "logistic_regression"
    
    # 6. Salvar melhor modelo
    model_dir = save_model(best_model, encoders, model_name, best_metrics)
    
    # 7. Registrar modelo no MLflow
    with mlflow.start_run(run_name=f"best_model_{model_name}"):
        mlflow.log_param("model_type", model_name)
        mlflow.log_metrics(best_metrics)
        mlflow.sklearn.log_model(
            best_model, 
            "model",
            registered_model_name="credit_score_classifier"
        )
    
    print("\n" + "="*60)
    print("TREINAMENTO CONCLUIDO!")
    print(f"   - Melhor modelo: {model_name}")
    print(f"   - F1-Score: {best_metrics['f1_score']:.4f}")
    print(f"   - Accuracy: {best_metrics['accuracy']:.4f}")
    print("\nPara visualizar experimentos:")
    print("   mlflow ui")
    print("="*60)

if __name__ == "__main__":
    main()