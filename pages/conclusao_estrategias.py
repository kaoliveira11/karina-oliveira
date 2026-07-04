# --- Importar o streamlit --- #
import streamlit as st
import io

from enviar_arquivos import enviar_email

# --- Configurações da página --- #
st.set_page_config(
    page_title='KData Insights',
    page_icon='💻',
    layout='wide'
)

st.title("💻 KData Insights")
st.subheader("Fechamento das análises")

if st.session_state.usuario:
    st.success(f"Olá, {st.session_state.usuario}! Seja bem-vindo(a) 😊")
else:
    st.info("Olá! Digite seu nome na barra lateral para personalizar sua experiência.")

st.divider()

st.markdown("📊 Visão Geral ")


st.write(
    """
    As análises permitiram identificar padrões de comportamento, 
    fatores de risco e oportunidades de retenção, oferecendo suporte à tomada de decisões estratégicas 
    para reduzir churn e fortalecer a relação com os clientes.
    """
)
st.divider()

st.markdown("🔎  **Por que os clientes estão saindo?**    ")
st.markdown("_O preço aparece, mas não é o vilão principal. O cliente quer custo-benefício e qualidade._")

st.markdown('**Pontos levantados sobre a Concorrência**:\n\n'
            '- Aparelhos mais modernos\n\n'
            '- Planos mais vantajosos\n\n'
            '- Mais dados incluídos\n\n'
            '- Internet mais rápida\n\n'
                )

st.markdown('**Reclamações sobre Atendimento**:\n\n'
            '- Suporte pouco eficiente\n\n'
            '- Atendimento ruim em geral\n\n'
            '- Rede instável e suporte online fraco\n\n'
                )
st.divider()

st.markdown("📅 **Quando o risco é maior?** ")
st.markdown("_Primeiro ano, quase metade dos cancelamentos acontece nos 12 meses iniciais._")

st.markdown('**Pontos observados no perfil de clientes que efetuam o cancelamento**:\n\n'
            '- Tipo de contrato: o mensal representa 46% dos cancelamentos em relação aos outros modelos\n\n'
            '- Clientes sêniores: representam 16% da base, mas 25% dos cancelamentos\n\n'
            '- Quem veio por indicação cancela muito menos (19,4% vs 32,6%)\n\n'
            '- A distribuição entre homens e mulheres é praticamente equilibrada tanto na base total quanto entre os clientes cancelados.\n\n'
                )
st.divider()

st.markdown("💰 **Impacto Financeiro** ")
st.markdown("_Além da perda de clientes, a empresa apresenta perdas expressivas de receita._")

st.markdown('**Os maiores impactos financeiros concentram-se exatamente nos mesmos motivos que lideram os cancelamentos:**\n\n'
            '- Ofertas melhores da concorrência\n\n'
            '- Dispositivos mais atrativos;\n\n'
            '- Problemas de atendimento\n\n')

st.markdown('**Os serviços que apresentam maior perda financeira são:**:\n\n'
            '- Internet\n\n'
            '- Telefonia;\n\n'
            '- Streaming\n\n')
st.divider()

st.markdown("🎯 **Insights que viram resultados** ")
st.markdown("_Retenção inicial e planos competitivos_")
st.write(
    """
   Metade dos cancelamentos acontece no primeiro ano, principalmente em contratos mensais, 
   e muitos clientes migram para concorrentes que oferecem mais dados e velocidade. 
   A solução é combinar um programa de acompanhamento nos primeiros meses com incentivos para contratos anuais, 
   além de revisar planos regularmente, ampliar franquias e melhorar a 
   qualidade técnica para tornar a oferta mais atrativa.
    """
)
st.markdown("💡 **Soluções**")
st.markdown('- Revisar planos com frequência, aumentar franquias e velocidade, '
            'incluir extras sem pesar no preço e investir em qualidade técnica\n\n'
            '- Fortalecer o programa de indicação (bonificação, cashback, descontos progressivos) '
            'e criar um programa de fidelidade\n\n'
            '- Treinar equipes de atendimento, reduzir tempo de espera, resolver no primeiro contato e, '
            'antes do cancelamento, oferecer ligações personalizadas\n\n'
            '- Atendimento simplificado e prioritário para sêniores, junto com melhorias na experiência digital\n\n')
st.divider()

# ============================
# DOWNLOAD E ENVIO DO RELATÓRIO
# ============================

relatorio_conclusao = """
📊 Visão Geral

As análises permitiram identificar padrões de comportamento,fatores de risco e oportunidades de retenção.
Oferecendo suporte à tomada de decisões estratégicas para reduzir churn e fortalecer a relação com os clientes.


🔎  Por que os clientes estão saindo?
O preço aparece, mas não é o vilão principal. O cliente quer custo-benefício e qualidade.

Pontos levantados sobre a Concorrência:
- Aparelhos mais modernos
- Planos mais vantajosos
- Mais dados incluídos
- Internet mais rápida

Reclamações sobre Atendimento:
- Suporte pouco eficiente
- Atendimento ruim em geral
- Rede instável e suporte online fraco

📅 Quando o risco é maior?
Primeiro ano, quase metade dos cancelamentos acontece nos 12 meses iniciais.

Pontos observados no perfil de clientes que efetuam o cancelamento:
- Tipo de contrato: o mensal representa 46% dos cancelamentos em relação aos outros modelos
- Clientes sêniores: representam 16% da base, mas 25% dos cancelamentos
- Quem veio por indicação cancela muito menos (19,4% vs 32,6%)
- A distribuição entre homens e mulheres é praticamente equilibrada tanto na base total quanto entre os clientes cancelados.

💰 Impacto Financeiro
Além da perda de clientes, a empresa apresenta perdas expressivas de receita.

Os maiores impactos financeiros concentram-se exatamente nos mesmos motivos que lideram os cancelamentos:
- Ofertas melhores da concorrência
- Dispositivos mais atrativos
- Problemas de atendimento

Os serviços que apresentam maior perda financeira são:
- Internet
- Telefonia
- Streaming

🎯Insights que viram resultados

Retenção inicial e planos competitivos:
Metade dos cancelamentos acontece no primeiro ano, principalmente em contratos mensais, 
e muitos clientes migram para concorrentes que oferecem mais dados e velocidade. 
A solução é combinar um programa de acompanhamento nos primeiros meses com incentivos para contratos anuais, 
além de revisar planos regularmente, ampliar franquias e melhorar a 
qualidade técnica para tornar a oferta mais atrativa.

💡 Soluções:
- Revisar planos com frequência, aumentar franquias e velocidade, incluir extras sem pesar no preço e investir em qualidade técnica
- Fortalecer o programa de indicação (bonificação, cashback, descontos progressivos) e criar um programa de fidelidade
- Treinar equipes de atendimento, reduzir tempo de espera, resolver no primeiro contato e, antes do cancelamento, oferecer ligações personalizadas
- Atendimento simplificado e prioritário para sêniores, junto com melhorias na experiência digital
"""

st.subheader("📄 Exportar relatório de conclusão")

col1, col2 = st.columns(2)

with col1:
    buffer_download = io.BytesIO()
    buffer_download.write(relatorio_conclusao.encode("utf-8"))
    buffer_download.seek(0)

    st.download_button(
        label="📥 Baixar relatório",
        data=buffer_download,
        file_name="relatorio_conclusao_churn.txt",
        mime="text/plain",
        use_container_width=True
    )

with col2:
    destinatario = st.text_input("Digite o e-mail do destinatário:")

    if st.button("✉️ Enviar por e-mail", use_container_width=True):

        if destinatario == "":
            st.warning("Digite um e-mail antes de enviar.")

        else:
            buffer_email = io.BytesIO()
            buffer_email.write(relatorio_conclusao.encode("utf-8"))
            buffer_email.seek(0)

            anexos = [
                {
                    "buffer": buffer_email,
                    "nome_arquivo": "relatorio_conclusao_churn.txt",
                    "tipo": "txt"
                }
            ]

            sucesso = enviar_email(
                remetente=st.secrets["REMETENTE"],
                senha=st.secrets["SENHA"],
                destinatario=destinatario,
                assunto="Relatório de Conclusão - Análise de Churn",
                corpo="Olá! Segue em anexo o relatório de conclusão da análise de churn.",
                anexos=anexos
            )

            if sucesso:
                st.success("Relatório enviado com sucesso!")

            else:
                st.error("Não foi possível enviar o relatório.")
