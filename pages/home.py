# --- Importar o streamlit --- #
import streamlit as st

# --- Configurações da página --- #
st.set_page_config(
    page_title='KData Insights',
    page_icon='💻',
    layout='wide'
)


st.title("💻 KData Insights")
st.subheader("Dashboard Estratégico")

st.divider()

st.markdown("## 👋 Bem-vindo!")

st.write(
    """
    As análises permitem identificar padrões de comportamento, 
    fatores de risco e oportunidades de retenção, oferecendo suporte à tomada de decisões estratégicas 
    para reduzir churn e fortalecer a relação com os clientes.
    """
)

st.divider()

# OBJETIVO

st.markdown("## 🎯 Objetivo das análises")

st.markdown("""
- Identificar os principais motivos de cancelamento dos clientes.
- Analisar o perfil dos clientes que cancelaram e dos que permaneceram.
- Avaliar contratos, serviços, tempo de permanência e métodos de pagamento.
- Apoiar decisões estratégicas para reduzir o Churn.
""")

st.divider()

# O QUE VOCÊ ENCONTRARÁ

st.markdown("## 📊 O que você encontrará")

st.markdown("""

- 📉 Análise de Churn (em números absolutos e dashboards)

- 🌐 Serviços Contratados X Churn

- 👥 Perfil dos Clientes X Churn

- 💡 Conclusões Estratégicas

""")


