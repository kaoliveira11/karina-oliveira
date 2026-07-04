import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_projeto.csv", sep=None, engine="python")

    df.columns = df.columns.str.strip()

    df["Monthly Charge"] = pd.to_numeric(df["Monthly Charge"], errors="coerce")
    df["Total Charges"] = pd.to_numeric(df["Total Charges"], errors="coerce")
    df["Total Revenue"] = pd.to_numeric(df["Total Revenue"], errors="coerce")
    df["Tenure in Months"] = pd.to_numeric(df["Tenure in Months"], errors="coerce")

    # Criar coluna Status
    df["Status"] = df["Churn Label"].map({
        "Yes": "Cancelado",
        "No": "Ativo"
    })

    return df


