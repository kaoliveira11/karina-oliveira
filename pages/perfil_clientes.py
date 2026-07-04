import streamlit as st
from indicadores.graficos import (
    grafico_genero,
    grafico_genero_cancelados,
    grafico_senior,
    grafico_senior_cancelados,
    grafico_satisfacao,
    grafico_indicacao
)

st.title("👥 Perfil dos Clientes")

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if st.session_state.usuario:
    st.success(f"Olá, {st.session_state.usuario}! Seja bem-vindo(a) 😊")
else:
    st.info("Olá! Digite seu nome na barra lateral para personalizar sua experiência.")

st.write(
    """
    Esta página apresenta características dos clientes e permite observar
    quais perfis possuem maior concentração de cancelamentos.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.pyplot(grafico_genero(), use_container_width=False)

with col2:
    st.pyplot(grafico_genero_cancelados(), use_container_width=False)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.pyplot(grafico_senior(), use_container_width=False)

with col2:
    st.pyplot(grafico_senior_cancelados(), use_container_width=False)

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.pyplot(grafico_satisfacao(), use_container_width=False)

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.pyplot(grafico_indicacao(), use_container_width=False)