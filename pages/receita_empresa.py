import streamlit as st
from indicadores.graficos import (
    grafico_cobranca_mensal,
    grafico_cobranca_total
)

st.title("💰 Receita e Cobranças")

st.write(
    """
    Esta página analisa a relação entre os valores cobrados dos clientes
    e o comportamento de cancelamento.
    """
)

st.divider()

st.plotly_chart(grafico_cobranca_mensal(), use_container_width=True)

st.divider()

st.plotly_chart(grafico_cobranca_total(), use_container_width=True)
