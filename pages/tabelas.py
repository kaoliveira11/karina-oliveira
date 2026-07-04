import streamlit as st
import pandas as pd
from indicadores.carregar_dados import carregar_dados


st.title("📑 Tabelas de Análise")
st.subheader("Dados absolutos")

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if st.session_state.usuario:
    st.success(f"Olá, {st.session_state.usuario}! Seja bem-vindo(a) 😊")
else:
    st.info("Olá! Digite seu nome na barra lateral para personalizar sua experiência.")

st.write(
    """
    Esta página apresenta tabelas estáticas com informações complementares
    sobre os cancelamentos dos clientes, expressas em números absolutos.
    """
)

st.divider()



st.subheader("Motivos de Cancelamento")

df = carregar_dados()

df_churn = df[df["Churn Label"] == "Yes"]

tabela_motivos = (
    df_churn
    .groupby("Churn Reason")
    .agg(
        Quantidade_de_Cancelamentos=("Customer ID", "count"),
        Receita_Perdida=("Total Revenue", "sum")
    )
    .reset_index()
)

tabela_motivos.columns = [
    "Motivo do Cancelamento",
    "Quantidade de Cancelamentos",
    "Receita Perdida"
]

total_cancelados = len(df_churn)

tabela_motivos["Percentual"] = (
    tabela_motivos["Quantidade de Cancelamentos"] / total_cancelados * 100
).round(1)

tabela_motivos["Percentual"] = tabela_motivos["Percentual"].astype(str) + "%"

# Traduzir motivos
tabela_motivos["Motivo do Cancelamento"] = tabela_motivos["Motivo do Cancelamento"].replace({
    "Competitor offered more data": "Concorrente ofereceu mais dados móveis",
    "Competitor made better offer": "Concorrente fez uma oferta melhor",
    "Limited range of services": "Portfólio limitado de serviços",
    "Extra data charges": "Cobranças extras por dados móveis",
    "Competitor had better devices": "Concorrente oferecia dispositivos melhores",
    "Don't know": "Não Informado",
    "Service dissatisfaction": "Insatisfação com o serviço",
    "Lack of affordable download/upload speed": "Velocidade de download/upload com custo elevado",
    "Product dissatisfaction": "Insatisfação com o produto",
    "Long distance charges": "Tarifas de chamadas de longa distância",
    "Poor expertise of online support": "Baixa qualidade do suporte online",
    "Attitude of support person": "Atendimento inadequado do suporte",
    "Network reliability": "Baixa confiabilidade da rede",
    "Competitor offered higher download speeds": "Concorrente ofereceu maior velocidade de download",
    "Moved": "Mudança de residência",
    "Price too high": "Preço muito alto",
    "Attitude of service provider": "Atendimento inadequado da empresa",
    "Poor expertise of phone support": "Baixa qualidade do suporte telefônico",
    "Deceased": "Falecimento",
    "Lack of self-service on Website": "Falta de autoatendimento no site"
})

tabela_motivos = tabela_motivos.sort_values(
    by="Quantidade de Cancelamentos",
    ascending=False
)

motivos = ["Todos"] + sorted(tabela_motivos["Motivo do Cancelamento"].unique())

filtro_motivo = st.selectbox(
    "Filtrar por motivo:",
    motivos
)

if filtro_motivo != "Todos":
    tabela_filtrada = tabela_motivos[
        tabela_motivos["Motivo do Cancelamento"] == filtro_motivo
    ]
else:
    tabela_filtrada = tabela_motivos

tabela_filtrada = tabela_filtrada.copy()

def formato_moeda(valor):
    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.table(tabela_filtrada)

st.divider()

# ============================
# TABELA 2 - RECEITA PERDIDA POR SERVIÇO
# ============================

st.subheader("Receita por Tipo de Serviço: Ativos x Cancelados")

servicos = [
    "Phone Service",
    "Internet Service",
    "Online Security",
    "Online Backup",
    "Device Protection Plan",
    "Premium Tech Support",
    "Streaming TV",
    "Streaming Movies",
    "Streaming Music",
    "Unlimited Data"
]

lista = []

for servico in servicos:

    df_servico = df[df[servico] == "Yes"]

    servicos_ativos = df_servico[df_servico["Churn Label"] == "No"].shape[0]
    servicos_cancelados = df_servico[df_servico["Churn Label"] == "Yes"].shape[0]

    receita_ativa = (
        df_servico[df_servico["Churn Label"] == "No"]["Total Revenue"]
        .sum()
    )

    receita_perdida = (
        df_servico[df_servico["Churn Label"] == "Yes"]["Total Revenue"]
        .sum()
    )

    total_receita = receita_ativa + receita_perdida

    if total_receita > 0:
        percentual_perda = receita_perdida / total_receita * 100
    else:
        percentual_perda = 0

    lista.append([
        servico,
        servicos_ativos,
        servicos_cancelados,
        receita_ativa,
        receita_perdida,
        percentual_perda
    ])

tabela_receita = pd.DataFrame(
    lista,
    columns=[
        "Serviços",
        "Contratos Ativos",
        "Contratos Cancelados",
        "Receita Ativa",
        "Receita Perdida",
        "% Perda"
    ]
)

tabela_receita = tabela_receita.sort_values(
    by="Receita Perdida",
    ascending=False
)

def formato_moeda(valor):
    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

tabela_receita["Receita Ativa"] = tabela_receita["Receita Ativa"].apply(formato_moeda)
tabela_receita["Receita Perdida"] = tabela_receita["Receita Perdida"].apply(formato_moeda)

tabela_receita["% Perda"] = (
    tabela_receita["% Perda"]
    .round(1)
    .astype(str)
    + "%"
)

st.table(tabela_receita)

st.divider()


st.subheader("Análise por Cidade")

df = carregar_dados()

cidades_selecionadas = st.multiselect(
    "Selecione as cidades:",
    options=sorted(df["City"].unique())
)

if cidades_selecionadas:
    df = df[df["City"].isin(cidades_selecionadas)]

tabela_cidades = (
    df.groupby("City")
    .agg(
        Total_Clientes=("Customer ID", "count"),
        Clientes_Cancelados=("Churn Label", lambda x: (x == "Yes").sum()),
        Receita_Perdida=(
            "Total Revenue",
            lambda x: x[df.loc[x.index, "Churn Label"] == "Yes"].sum()
        )
    )
    .reset_index()
)

tabela_cidades["Taxa de Churn"] = (
    tabela_cidades["Clientes_Cancelados"] /
    tabela_cidades["Total_Clientes"] * 100
).round(1)

tabela_cidades = tabela_cidades.sort_values(
    by="Total_Clientes",
    ascending=False
).head(10)

tabela_cidades["Taxa de Churn"] = (
    tabela_cidades["Taxa de Churn"].astype(str) + "%"
)

tabela_cidades["Receita Perdida"] = (
    tabela_cidades["Receita_Perdida"]
    .map(lambda x: f"R$ {x:,.2f}")
)

tabela_cidades = tabela_cidades[[
    "City",
    "Total_Clientes",
    "Clientes_Cancelados",
    "Taxa de Churn",
    "Receita Perdida"
]]

tabela_cidades.columns = [
    "Cidade",
    "Total de Clientes",
    "Clientes Cancelados",
    "Taxa de Churn",
    "Receita Perdida"
]

st.table(tabela_cidades)