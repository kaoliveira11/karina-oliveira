import streamlit as st

st.set_page_config(
    page_title="Dashboard Churn",
    page_icon="📉",
    layout="wide"
)

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

st.sidebar.title("👤 Usuário")

st.session_state.usuario = st.sidebar.text_input(
    "Digite seu nome:",
    value=st.session_state.usuario
)

pg = st.navigation(
    [
        st.Page('./pages/home.py',
                title='Início',
                icon='🏠'),

        st.Page('./pages/churn.py',
                title='Análise de Churn',
                icon='📉'),

        st.Page('./pages/tabelas.py',
                title='Dados Analíticos - Tabelas',
                icon='📑'),

        st.Page('./pages/perfil_clientes.py',
                title='Perfil dos Clientes x Churn',
                icon='👥'),

st.Page('./pages/conclusao_estrategias.py',
                title='Síntese dos Resultados',
                icon='💡'),

st.Page('./pages/enviar_graficos.py',
                title='Enviar gráficos por email',
                icon='✉️'),
    ]
)

pg.run()