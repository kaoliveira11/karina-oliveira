import streamlit as st
import io
import matplotlib.pyplot as plt

from indicadores.graficos import (
    grafico_status_clientes,
    grafico_motivos_churn,
    grafico_contrato_churn,
    grafico_tempo_permanencia,
    grafico_genero,
    grafico_genero_cancelados,
    grafico_senior,
    grafico_senior_cancelados,
    grafico_pagamento_churn,
    grafico_satisfacao,
    grafico_indicacao
)

from enviar_arquivos import enviar_email


st.title("📧 Envio de Gráficos por E-mail")

if st.session_state.usuario:
    st.success(f"Olá, {st.session_state.usuario}! Seja bem-vindo(a) 😊")
else:
    st.info("Olá! Digite seu nome na barra lateral para personalizar sua experiência.")

st.write("Selecione um ou mais gráficos estáticos e envie para o e-mail desejado.")

destinatario = st.text_input("Digite o e-mail do destinatário")

opcoes_graficos = {
    "Status dos Clientes": {
        "funcao": grafico_status_clientes,
        "arquivo": "status_clientes.png"
    },
    "Motivos de Churn": {
        "funcao": grafico_motivos_churn,
        "arquivo": "motivos_churn.png"
    },
    "Churn por Contrato": {
        "funcao": grafico_contrato_churn,
        "arquivo": "churn_contrato.png"
    },
    "Tempo de Permanência": {
        "funcao": grafico_tempo_permanencia,
        "arquivo": "tempo_permanencia.png"
    },
    "Perfil por Gênero": {
        "funcao": grafico_genero,
        "arquivo": "perfil_genero.png"
    },
    "Cancelamentos por Gênero": {
        "funcao": grafico_genero_cancelados,
        "arquivo": "cancelamentos_genero.png"
    },
    "Perfil Sênior": {
        "funcao": grafico_senior,
        "arquivo": "perfil_senior.png"
    },
    "Cancelamentos Sênior": {
        "funcao": grafico_senior_cancelados,
        "arquivo": "cancelamentos_senior.png"
    },
    "Forma de Pagamento": {
        "funcao": grafico_pagamento_churn,
        "arquivo": "forma_pagamento.png"
    },
    "Satisfação dos Clientes": {
        "funcao": grafico_satisfacao,
        "arquivo": "satisfacao_clientes.png"
    },
    "Indicação x Churn": {
        "funcao": grafico_indicacao,
        "arquivo": "indicacao_churn.png"
    }
}

graficos_escolhidos = st.multiselect(
    "Selecione os gráficos:",
    list(opcoes_graficos.keys())
)

if st.button("Enviar gráficos por e-mail"):

    if destinatario == "":
        st.warning("Digite um e-mail antes de enviar.")

    elif len(graficos_escolhidos) == 0:
        st.warning("Selecione pelo menos um gráfico.")

    else:
        anexos = []

        for grafico in graficos_escolhidos:
            buffer = io.BytesIO()

            fig = opcoes_graficos[grafico]["funcao"]()
            fig.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)

            anexos.append({
                "buffer": buffer,
                "nome_arquivo": opcoes_graficos[grafico]["arquivo"],
                "tipo": "imagem"
            })

            plt.close(fig)

        sucesso = enviar_email(
            remetente=st.secrets["REMETENTE"],
            senha=st.secrets["SENHA"],
            destinatario=destinatario,
            assunto="Gráficos Estáticos - Análise de Churn",
            corpo=(
                "Olá!\n\n"
                "Seguem em anexo os gráficos solicitados no relatório de análise de churn.\n\n"
                "Atenciosamente,\n"
                "KData Insights"
            ),

            anexos=anexos
        )


        if sucesso:
            st.success("E-mail enviado com sucesso!")

        else:
            st.error("Não foi possível enviar o e-mail.")