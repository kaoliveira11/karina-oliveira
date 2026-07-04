import streamlit as st
from indicadores.indicadores import calcular_indicadores
from indicadores.graficos import (
    grafico_status_clientes,
    grafico_motivos_churn,
    grafico_contrato_churn,
    grafico_tempo_permanencia,
    grafico_pagamento_churn,
)

st.title("📉 Análise de Churn")

if st.session_state.usuario:
    st.success(f"Olá, {st.session_state.usuario}! Seja bem-vindo(a) 😊")
else:
    st.info("Olá! Digite seu nome na barra lateral para personalizar sua experiência.")

st.write(
    """
    Esta página apresenta os principais indicadores e gráficos relacionados
    ao cancelamento dos clientes.
    """
)

# ============================
# INDICADORES
# ============================

total, ativos, cancelados, taxa = calcular_indicadores()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Clientes", total)
col2.metric("Clientes Ativos", ativos)
col3.metric("Clientes Cancelados", cancelados)
col4.metric("Taxa de Churn", f"{taxa:.2f}%")

st.divider()

# ============================
# STATUS x MOTIVOS
# ============================

col1, col2 = st.columns(2)

with col1:
    st.pyplot(grafico_status_clientes(), use_container_width=False)

with col2:
    st.pyplot(grafico_motivos_churn(), use_container_width=False)

st.divider()

# ============================
# CONTRATO x PAGAMENTO
# ============================

col1, col2 = st.columns(2)

with col1:
    st.pyplot(grafico_contrato_churn(), use_container_width=False)

with col2:
    st.pyplot(grafico_pagamento_churn(), use_container_width=False)

st.divider()

# ============================
# TEMPO DE PERMANÊNCIA
# ============================

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.pyplot(grafico_tempo_permanencia(), use_container_width=False)