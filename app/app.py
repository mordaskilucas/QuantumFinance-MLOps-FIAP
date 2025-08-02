# -*- coding: utf-8 -*-
"""
Aplicacao Streamlit - QuantumFinance Score de Credito
Autores:
 357103 - Víctor Kennedy Kaneko Nunes
 358078 - Octavio Ribeiro
 360075 - Gabriel Oliveira
 358032 - Lucas Guilherme Mordaski
Data: 2025

Interface web para predicao de score de credito integrada com a API.
"""

import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import time

# Configuracao da pagina
st.set_page_config(
    page_title="QuantumFinance - Score de Crédito",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da API
API_URL = "http://localhost:8001"

# Estilo customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .good-score {
        background-color: #E8F5E9;
        border: 2px solid #4CAF50;
    }
    .standard-score {
        background-color: #FFF8E1;
        border: 2px solid #FFC107;
    }
    .poor-score {
        background-color: #FFEBEE;
        border: 2px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessao
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None

def check_api_health():
    """Verifica se a API esta online."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def login(username, password):
    """Realiza login na API."""
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.username = username
            return True
        return False
    except:
        return False

def predict_score(data):
    """Faz predicao de score usando a API."""
    headers = {
        "Authorization": f"Bearer {st.session_state.token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.session_state.token = None
            st.error("Sessão expirada. Faça login novamente.")
            return None
        else:
            st.error(f"Erro na predição: {response.text}")
            return None
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return None

def main():
    """Funcao principal da aplicacao."""
    
    # Header
    st.markdown('<h1 class="main-header">QuantumFinance Score de Crédito</h1>', unsafe_allow_html=True)
    
    # Verificar status da API
    api_status = check_api_health()
    
    # Sidebar
    with st.sidebar:
        st.title("Configurações")
        
        # Status da API
        if api_status:
            st.success("API Online")
        else:
            st.error("API Offline")
            st.warning("Certifique-se de que a API está rodando em http://localhost:8000")
        
        # Login
        st.subheader("Autenticação")
        
        if st.session_state.token is None:
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            
            if st.button("Login"):
                if login(username, password):
                    st.success(f"Bem-vindo, {username}!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
            
            st.info("**Usuários de teste:**\n- admin / quantumfinance123\n- analista / quantumfinance123")
        else:
            st.success(f"Logado como: {st.session_state.username}")
            if st.button("Logout"):
                st.session_state.token = None
                st.session_state.username = None
                st.rerun()
    
    # Conteudo principal
    if st.session_state.token is None:
        st.warning("Faça login para usar o sistema")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Análise Individual", "Análise em Lote", "Sobre"])
    
    # Tab 1: Analise Individual
    with tab1:
        st.header("Análise de Score de Crédito Individual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Informações Pessoais")
            age = st.number_input("Idade", min_value=18, max_value=100, value=35)
            occupation = st.text_input("Ocupação", value="Engineer")
            
            st.subheader("Informações Financeiras")
            annual_income = st.number_input("Renda Anual (R$)", min_value=0.0, value=120000.0, step=1000.0)
            monthly_inhand_salary = st.number_input("Salário Líquido Mensal (R$)", min_value=0.0, value=8500.0, step=100.0)
            num_bank_accounts = st.number_input("Número de Contas Bancárias", min_value=0, value=3)
            num_credit_card = st.number_input("Número de Cartões de Crédito", min_value=0, value=2)
            
        with col2:
            st.subheader("Informações de Crédito")
            interest_rate = st.number_input("Taxa de Juros (%)", min_value=0.0, max_value=100.0, value=12.5)
            num_of_loan = st.number_input("Número de Empréstimos", min_value=0, value=2)
            type_of_loan = st.text_input("Tipos de Empréstimo", value="Auto Loan, Personal Loan")
            outstanding_debt = st.number_input("Dívida Pendente (R$)", min_value=0.0, value=25000.0, step=1000.0)
            credit_utilization_ratio = st.number_input("Taxa de Utilização de Crédito (%)", min_value=0.0, max_value=100.0, value=35.5)
            
        st.subheader("Histórico de Pagamentos")
        col3, col4 = st.columns(2)
        
        with col3:
            delay_from_due_date = st.number_input("Dias de Atraso", min_value=-30, max_value=365, value=5)
            num_of_delayed_payment = st.number_input("Número de Pagamentos Atrasados", min_value=0, value=1)
            changed_credit_limit = st.number_input("Mudança no Limite (%)", value=5.0)
            num_credit_inquiries = st.number_input("Consultas de Crédito", min_value=0, value=2)
            
        with col4:
            credit_mix = st.selectbox("Mix de Crédito", ["Good", "Standard", "Bad"], index=0)
            credit_history_age = st.text_input("Idade do Histórico", value="5 Years and 2 Months")
            payment_of_min_amount = st.selectbox("Paga Valor Mínimo?", ["Yes", "No"], index=0)
            
        st.subheader("Comportamento Financeiro")
        col5, col6 = st.columns(2)
        
        with col5:
            total_emi_per_month = st.number_input("Total EMI Mensal (R$)", min_value=0.0, value=2500.0)
            amount_invested_monthly = st.number_input("Investimento Mensal (R$)", min_value=0.0, value=1500.0)
            
        with col6:
            payment_behaviour = st.selectbox(
                "Comportamento de Pagamento",
                ["Low_spent_Small_value_payments", "Low_spent_Medium_value_payments", 
                 "Low_spent_Large_value_payments", "High_spent_Small_value_payments",
                 "High_spent_Medium_value_payments", "High_spent_Large_value_payments"],
                index=1
            )
            monthly_balance = st.number_input("Saldo Mensal (R$)", value=15000.0)
        
        # Botao de predicao
        if st.button("Analisar Score de Crédito", type="primary"):
            with st.spinner("Analisando dados..."):
                # Preparar dados
                data = {
                    "age": age,
                    "occupation": occupation,
                    "annual_income": annual_income,
                    "monthly_inhand_salary": monthly_inhand_salary,
                    "num_bank_accounts": num_bank_accounts,
                    "num_credit_card": num_credit_card,
                    "interest_rate": interest_rate,
                    "num_of_loan": num_of_loan,
                    "type_of_loan": type_of_loan,
                    "delay_from_due_date": delay_from_due_date,
                    "num_of_delayed_payment": num_of_delayed_payment,
                    "changed_credit_limit": changed_credit_limit,
                    "num_credit_inquiries": num_credit_inquiries,
                    "credit_mix": credit_mix,
                    "outstanding_debt": outstanding_debt,
                    "credit_utilization_ratio": credit_utilization_ratio,
                    "credit_history_age": credit_history_age,
                    "payment_of_min_amount": payment_of_min_amount,
                    "total_emi_per_month": total_emi_per_month,
                    "amount_invested_monthly": amount_invested_monthly,
                    "payment_behaviour": payment_behaviour,
                    "monthly_balance": monthly_balance
                }
                
                # Fazer predicao
                result = predict_score(data)
                
                if result:
                    # Mostrar resultado
                    st.success("Análise concluída!")
                    
                    # Determinar classe CSS
                    score_class = ""
                    if result["credit_score"] == "Good":
                        score_class = "good-score"
                    elif result["credit_score"] == "Standard":
                        score_class = "standard-score"
                    else:
                        score_class = "poor-score"
                    
                    # Mostrar resultado em destaque
                    st.markdown(f"""
                    <div class="result-box {score_class}">
                        <h2 style="text-align: center;">Score de Crédito: {result["credit_score"]}</h2>
                        <p style="text-align: center; font-size: 1.2rem;">Confiança: {result["confidence"]:.1%}</p>
                        <p style="text-align: center;">Nível de Risco: {result["risk_level"]}</p>
                        <hr>
                        <p><strong>Recomendação:</strong> {result["recommendation"]}</p>
                        <p><small>ID da Predição: {result["prediction_id"]} | {result["timestamp"]}</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Metricas adicionais
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score", result["credit_score"])
                    with col2:
                        st.metric("Confiança", f"{result['confidence']:.1%}")
                    with col3:
                        st.metric("Risco", result["risk_level"])
    
    # Tab 2: Analise em Lote
    with tab2:
        st.header("Análise de Score de Crédito em Lote")
        
        st.info("Faça upload de um arquivo CSV com os dados dos clientes para análise em lote.")
        
        # Template CSV
        if st.button("Baixar Template CSV"):
            template_data = {
                "age": [35, 45],
                "occupation": ["Engineer", "Manager"],
                "annual_income": [120000, 200000],
                "monthly_inhand_salary": [8500, 15000],
                "num_bank_accounts": [3, 5],
                "num_credit_card": [2, 4],
                "interest_rate": [12.5, 8.0],
                "num_of_loan": [2, 3],
                "type_of_loan": ["Auto Loan, Personal Loan", "Home Loan, Auto Loan"],
                "delay_from_due_date": [5, 0],
                "num_of_delayed_payment": [1, 0],
                "changed_credit_limit": [5.0, 10.0],
                "num_credit_inquiries": [2, 1],
                "credit_mix": ["Good", "Good"],
                "outstanding_debt": [25000, 50000],
                "credit_utilization_ratio": [35.5, 20.0],
                "credit_history_age": ["5 Years", "15 Years"],
                "payment_of_min_amount": ["Yes", "Yes"],
                "total_emi_per_month": [2500, 5000],
                "amount_invested_monthly": [1500, 5000],
                "payment_behaviour": ["Low_spent_Medium_value_payments", "Low_spent_Large_value_payments"],
                "monthly_balance": [15000, 50000]
            }
            
            template_df = pd.DataFrame(template_data)
            csv = template_df.to_csv(index=False)
            st.download_button(
                label="Download Template",
                data=csv,
                file_name="template_credit_score.csv",
                mime="text/csv"
            )
        
        # Upload arquivo
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])
        
        if uploaded_file is not None:
            # Ler arquivo
            df = pd.read_csv(uploaded_file)
            st.write(f"{len(df)} clientes carregados")
            
            # Mostrar preview
            st.subheader("Preview dos Dados")
            st.dataframe(df.head())
            
            # Botao para processar
            if st.button("Processar Lote", type="primary"):
                with st.spinner(f"Processando {len(df)} clientes..."):
                    # Preparar dados para API
                    predictions = df.to_dict('records')
                    batch_data = {"predictions": predictions}
                    
                    # Fazer requisicao
                    headers = {
                        "Authorization": f"Bearer {st.session_state.token}",
                        "Content-Type": "application/json"
                    }
                    
                    try:
                        response = requests.post(
                            f"{API_URL}/predict/batch",
                            json=batch_data,
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.success(f"Processamento concluído em {result['processing_time']:.2f}s")
                            
                            # Processar resultados
                            results_data = []
                            for i, pred in enumerate(result['results']):
                                row = df.iloc[i].to_dict()
                                row['credit_score'] = pred['credit_score']
                                row['confidence'] = pred['confidence']
                                row['risk_level'] = pred['risk_level']
                                results_data.append(row)
                            
                            results_df = pd.DataFrame(results_data)
                            
                            # Mostrar estatisticas
                            st.subheader("Estatísticas dos Resultados")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                score_counts = results_df['credit_score'].value_counts()
                                st.metric("Good", score_counts.get('Good', 0))
                            with col2:
                                st.metric("Standard", score_counts.get('Standard', 0))
                            with col3:
                                st.metric("Poor", score_counts.get('Poor', 0))
                            
                            # Mostrar resultados
                            st.subheader("Resultados Detalhados")
                            st.dataframe(
                                results_df[['age', 'occupation', 'annual_income', 
                                          'credit_score', 'confidence', 'risk_level']]
                            )
                            
                            # Download resultados
                            csv_results = results_df.to_csv(index=False)
                            st.download_button(
                                label="Download Resultados",
                                data=csv_results,
                                file_name=f"resultados_credit_score_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        else:
                            st.error(f"Erro no processamento: {response.text}")
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
    
    # Tab 3: Sobre
    with tab3:
        st.header("Sobre o Sistema")
        
        st.markdown("""
        ### QuantumFinance Score de Crédito
        
        Sistema desenvolvido para análise automatizada de score de crédito usando Machine Learning.
        
        #### Características:
        - **Modelo**: Random Forest com 77.5% de acurácia
        - **Features**: 25 variáveis incluindo informações financeiras e comportamentais
        - **API**: FastAPI com autenticação JWT e rate limiting
        - **Interface**: Streamlit para fácil utilização
        
        #### Classificações:
        - **Good**: Cliente com baixo risco, elegível para melhores condições
        - **Standard**: Cliente com risco médio, condições padrão
        - **Poor**: Cliente com alto risco, requer análise adicional
        
        #### Tecnologias:
        - Python, Scikit-learn, MLflow
        - FastAPI, JWT Authentication
        - Streamlit, Pandas
        
        #### Desenvolvimento:
        Projeto desenvolvido como trabalho de MLOps - MBA FIAP
        """)

if __name__ == "__main__":
    main()