import matplotlib.pyplot as plt
import pandas as pd
from indicadores.carregar_dados import carregar_dados


def criar_figura(largura=4.2, altura=2.6):
    fig, ax = plt.subplots(figsize=(largura, altura), dpi=90)
    return fig, ax

## Status Clientes ##
def grafico_status_clientes():
    df = carregar_dados()

    dados = df["Status"].value_counts()

    cores = []
    for status in dados.index:
        if status == "Ativo":
            cores.append("darkgreen")
        else:
            cores.append("salmon")

    fig, ax = criar_figura(3.4, 2.4)

    ax.pie(
        dados.values,
        labels=dados.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        radius=0.65,
        textprops={"fontsize": 5}
    )

    ax.set_title(
        "Contratos Ativos x Cancelados",
        fontsize=8,
        fontweight="bold"
    )

    ax.axis("equal")
    fig.subplots_adjust(top=0.82, bottom=0.05)

    return fig

# Chrun por tipo de contrato #
def grafico_motivos_churn():
    df = carregar_dados()

    df_churn = df[df["Churn Label"] == "Yes"]

    dados = (
        df_churn["Churn Category"]
        .value_counts()
        .head(8)
        .reset_index()
    )

    dados.columns = ["Motivo", "Quantidade"]

    dados = dados.sort_values(by="Quantidade", ascending=True)

    total_cancelados = len(df_churn)

    dados["Percentual"] = (
        dados["Quantidade"] / total_cancelados * 100
    ).round(1)

    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=100)

    barras = ax.barh(
        dados["Motivo"],
        dados["Quantidade"],
        color="tan",
        height=0.55
    )

    maior_valor = dados["Quantidade"].max()

    for barra, quantidade, percentual in zip(
        barras,
        dados["Quantidade"],
        dados["Percentual"]
    ):
        ax.text(
            barra.get_width() + (maior_valor * 0.02),
            barra.get_y() + barra.get_height() / 2,
            f"{quantidade} ({percentual}%)",
            va="center",
            fontsize=5
        )

    ax.set_title(
        "Top 10 Motivos de Cancelamento",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_xlim(0, maior_valor * 1.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.tick_params(axis="y", labelsize=7)

    ax.grid(False)

    fig.subplots_adjust(
        left=0.32,
        right=0.92,
        top=0.82,
        bottom=0.08
    )

    return fig

# Churn por tempo de contrato #
def grafico_contrato_churn():

    df = carregar_dados()

    dados = (
        df.groupby("Contract")
        .agg(
            Total_Clientes=("Customer ID", "count"),
            Clientes_Cancelados=("Churn Label", lambda x: (x == "Yes").sum())
        )
        .reset_index()
    )

    dados["Taxa de Churn"] = (
        dados["Clientes_Cancelados"] / dados["Total_Clientes"] * 100
    ).round(1)

    dados["Contract"] = dados["Contract"].replace({
        "Month-to-Month": "Mensal",
        "One Year": "1 Ano",
        "Two Year": "2 Anos"
    })

    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=100)

    barras = ax.bar(
        dados["Contract"],
        dados["Taxa de Churn"],
        color="tan",
        width=0.35
    )

    maior = dados["Taxa de Churn"].max()

    for barra, cancelados, taxa in zip(
            barras,
            dados["Clientes_Cancelados"],
            dados["Taxa de Churn"]):

        ax.text(
            barra.get_x() + barra.get_width()/2,
            barra.get_height() + 0.3,
            f"{cancelados}\n({taxa:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=5
        )

    ax.set_title(
        "Churn por Tipo de Contrato",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_ylim(0, maior * 1.30)

    ax.tick_params(axis="x", labelsize=5)
    ax.tick_params(axis="y", left=False, labelleft=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.grid(False)

    fig.subplots_adjust(
        left=0.08,
        right=0.98,
        top=0.82,
        bottom=0.20
    )

    return fig

# Chrun por tempo de permanencia (meses) #
def grafico_tempo_permanencia():

    df = carregar_dados()

    df["Faixa Permanência"] = pd.cut(
        df["Tenure in Months"],
        bins=[0, 12, 24, 36, 48, 60, 72],
        labels=[
            "0-12 meses",
            "13-24 meses",
            "25-36 meses",
            "37-48 meses",
            "49-60 meses",
            "61-72 meses"
        ],
        include_lowest=True
    )

    dados = (
        df.groupby("Faixa Permanência")
        .agg(
            Total_Clientes=("Customer ID", "count"),
            Clientes_Cancelados=("Churn Label", lambda x: (x == "Yes").sum())
        )
        .reset_index()
    )

    dados["Taxa de Churn"] = (
        dados["Clientes_Cancelados"] / dados["Total_Clientes"] * 100
    ).round(1)

    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=100)

    barras = ax.bar(
        dados["Faixa Permanência"].astype(str),
        dados["Taxa de Churn"],
        color="tan",
        width=0.55
    )

    maior = dados["Taxa de Churn"].max()

    for barra, cancelados, taxa in zip(
        barras,
        dados["Clientes_Cancelados"],
        dados["Taxa de Churn"]
    ):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.8,
            f"{cancelados}\n({taxa:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=6.5
        )

    ax.set_title(
        "Churn por Tempo de Contrato",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_ylim(0, maior * 1.30)

    ax.tick_params(axis="x", labelsize=6, rotation=20)
    ax.tick_params(axis="y", left=False, labelleft=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.grid(False)

    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        top=0.82,
        bottom=0.30
    )

    return fig

# Chrun por tipo de pagamento #
def grafico_pagamento_churn():

    df = carregar_dados()

    dados = (
        df.groupby("Payment Method")
        .agg(
            Total_Clientes=("Customer ID", "count"),
            Clientes_Cancelados=("Churn Label", lambda x: (x == "Yes").sum())
        )
        .reset_index()
    )

    dados["Taxa de Churn"] = (
        dados["Clientes_Cancelados"] / dados["Total_Clientes"] * 100
    ).round(1)

    dados["Payment Method"] = dados["Payment Method"].replace({
        "Mailed Check": "Cheque",
        "Bank Withdrawal": "Débito Automático",
        "Credit Card": "Cartão",
        "Electronic Check": "Cheque Eletrônico"
    })

    dados = dados.sort_values("Taxa de Churn", ascending=False)

    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=100)

    barras = ax.bar(
        dados["Payment Method"],
        dados["Taxa de Churn"],
        color="tan",
        width=0.50
    )

    maior = dados["Taxa de Churn"].max()

    for barra, cancelados, taxa in zip(
        barras,
        dados["Clientes_Cancelados"],
        dados["Taxa de Churn"]
    ):

        ax.text(
            barra.get_x() + barra.get_width()/2,
            barra.get_height() + 0.8,
            f"{cancelados}\n({taxa:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=6.5
        )

    ax.set_title(
        "Churn por Método de Pagamento",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_ylim(0, maior * 1.30)

    ax.tick_params(axis="x", labelsize=6, rotation=18)
    ax.tick_params(axis="y", left=False, labelleft=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.grid(False)

    fig.subplots_adjust(
        left=0.06,
        right=0.98,
        top=0.82,
        bottom=0.33
    )

    return fig

# -- GRAFICO GENERO - ##
def grafico_genero():

    df = carregar_dados()

    dados = df["Gender"].value_counts()

    dados.index = dados.index.map({
        "Male": "Masculino",
        "Female": "Feminino"
    })

    cores = []
    for genero in dados.index:
        if genero == "Masculino":
            cores.append("skyblue")
        elif genero == "Feminino":
            cores.append("pink")
        else:
            cores.append("gray")

    fig, ax = plt.subplots(figsize=(3.8, 2.8), dpi=100)

    ax.pie(
        dados.values,
        labels=dados.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        radius=0.68,
        textprops={"fontsize": 7}
    )

    ax.set_title(
        "Clientes por Gênero",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.axis("equal")

    fig.subplots_adjust(
        left=0.05,
        right=0.95,
        top=0.82,
        bottom=0.05
    )

    return fig

# -- GRAFICO GENERO CANCELADOS - ##
def grafico_genero_cancelados():

    df = carregar_dados()

    df_churn = df[df["Churn Label"] == "Yes"]

    dados = df_churn["Gender"].value_counts()

    dados.index = dados.index.map({
        "Male": "Masculino",
        "Female": "Feminino"
    })

    cores = []
    for genero in dados.index:
        if genero == "Masculino":
            cores.append("skyblue")
        elif genero == "Feminino":
            cores.append("pink")
        else:
            cores.append("gray")

    fig, ax = plt.subplots(figsize=(3.8, 2.8), dpi=100)

    ax.pie(
        dados.values,
        labels=dados.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        radius=0.68,
        textprops={"fontsize": 7}
    )

    ax.set_title(
        "Cancelamentos por Gênero",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.axis("equal")

    fig.subplots_adjust(
        left=0.05,
        right=0.95,
        top=0.82,
        bottom=0.05
    )

    return fig

# - GRÁFICO SÊNIOR - #
def grafico_senior():

    df = carregar_dados()

    dados = df["Senior Citizen"].value_counts()

    dados.index = dados.index.map({
        "Yes": "Sênior",
        "No": "Não Sênior"
    })

    cores = []
    for categoria in dados.index:
        if categoria == "Sênior":
            cores.append("beige")
        elif categoria == "Não Sênior":
            cores.append("teal")
        else:
            cores.append("lightgray")

    fig, ax = plt.subplots(figsize=(3.8, 2.8), dpi=100)

    ax.pie(
        dados.values,
        labels=dados.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        radius=0.68,
        textprops={"fontsize": 7}
    )

    ax.set_title(
        "Clientes Sênior x Não Sênior",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.axis("equal")

    fig.subplots_adjust(
        left=0.05,
        right=0.95,
        top=0.82,
        bottom=0.05
    )

    return fig

# - GRÁFICO SÊNIOR CANCELADOS - #
def grafico_senior_cancelados():

    df = carregar_dados()

    df_churn = df[df["Churn Label"] == "Yes"]

    dados = df_churn["Senior Citizen"].value_counts()

    dados.index = dados.index.map({
        "Yes": "Sênior",
        "No": "Não Sênior"
    })

    cores = []
    for categoria in dados.index:
        if categoria == "Sênior":
            cores.append("beige")
        elif categoria == "Não Sênior":
            cores.append("teal")
        else:
            cores.append("lightgray")

    fig, ax = plt.subplots(figsize=(3.8, 2.8), dpi=100)

    ax.pie(
        dados.values,
        labels=dados.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        radius=0.68,
        textprops={"fontsize": 7}
    )

    ax.set_title(
        "Cancelamentos: Sênior x Não Sênior",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.axis("equal")

    fig.subplots_adjust(
        left=0.05,
        right=0.95,
        top=0.82,
        bottom=0.05
    )

    return fig

# -- GRAFICO SATISFAÇÃO - ##
def grafico_satisfacao():

    df = carregar_dados()

    dados = df["Satisfaction Score"].value_counts().sort_index()

    cores = [
        "#E74C3C",
        "#E67E22",
        "#F1C40F",
        "#3498DB",
        "#2ECC71"
    ]

    fig, ax = plt.subplots(figsize=(4.2, 2.8), dpi=100)

    ax.pie(
        dados.values,
        labels=dados.index.astype(str),
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        radius=0.62,
        textprops={"fontsize": 7}
    )

    ax.set_title(
        "Índice de Satisfação",
        fontsize=8,
        fontweight="bold",
        pad=6
    )

    ax.legend(
        title="Nota",
        labels=dados.index.astype(str),
        loc="center left",
        bbox_to_anchor=(0.88, 0.5),
        fontsize=6,
        title_fontsize=7,
        frameon=False
    )

    ax.axis("equal")

    fig.subplots_adjust(
        left=0.02,
        right=0.82,
        top=0.82,
        bottom=0.05
    )

    return fig

# -- GRAFICO INDICAÇÃO X CHURN - ##

def grafico_indicacao():

    df = carregar_dados()

    dados = (
        df.groupby("Referred a Friend")
        .agg(
            Total_Clientes=("Customer ID", "count"),
            Clientes_Cancelados=("Churn Label", lambda x: (x == "Yes").sum())
        )
        .reset_index()
    )

    dados["Taxa_Churn"] = (
        dados["Clientes_Cancelados"] / dados["Total_Clientes"] * 100
    ).round(1)

    dados["Referred a Friend"] = dados["Referred a Friend"].replace({
        "Yes": "Indicados",
        "No": "Não Indicados"
    })

    dados = dados.set_index("Referred a Friend").loc[
        ["Indicados", "Não Indicados"]
    ].reset_index()

    fig, ax1 = plt.subplots(figsize=(3.6, 3.2), dpi=100)

    barras = ax1.bar(
        dados["Referred a Friend"],
        dados["Total_Clientes"],
        color=["turquoise", "teal"],
        width=0.45
    )

    maior_total = dados["Total_Clientes"].max()

    for barra, total in zip(barras, dados["Total_Clientes"]):
        ax1.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + (maior_total * 0.03),
            f"{total:,}".replace(",", ".") + "\nclientes",
            ha="center",
            va="bottom",
            fontsize=7,
            fontweight="bold"
        )

    ax2 = ax1.twinx()

    ax2.plot(
        dados["Referred a Friend"],
        dados["Taxa_Churn"],
        marker="o",
        linewidth=2,
        color="tan"
    )

    for x, taxa in zip(dados["Referred a Friend"], dados["Taxa_Churn"]):
        ax2.text(
            x,
            taxa + 1,
            f"{taxa:.1f}% churn",
            ha="center",
            va="bottom",
            fontsize=7,
            fontweight="bold"
        )

    ax1.set_title(
        "Programa de Indicação x Taxa de Churn",
        fontsize=9,
        fontweight="bold",
        pad=8
    )

    ax1.set_ylim(0, maior_total * 1.30)
    ax2.set_ylim(0, dados["Taxa_Churn"].max() * 1.45)

    ax1.set_xlabel("")
    ax1.set_ylabel("")
    ax2.set_ylabel("")

    ax1.tick_params(axis="x", labelsize=8, bottom=False)
    ax1.tick_params(axis="y", left=False, labelleft=False)
    ax2.tick_params(axis="y", right=False, labelright=False)

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)

    ax1.grid(False)
    ax2.grid(False)

    fig.subplots_adjust(
        left=0.04,
        right=0.80,
        top=0.75,
        bottom=0.10
    )

    return fig