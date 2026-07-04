from indicadores.carregar_dados import carregar_dados


def calcular_indicadores():
    df = carregar_dados()

    total_clientes = df["Customer ID"].nunique()
    clientes_cancelados = df[df["Churn Label"] == "Yes"]["Customer ID"].nunique()
    clientes_ativos = df[df["Churn Label"] == "No"]["Customer ID"].nunique()
    taxa_churn = clientes_cancelados / total_clientes * 100

    return total_clientes, clientes_ativos, clientes_cancelados, taxa_churn

