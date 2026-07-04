import streamlit as st
import smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


def enviar_email(remetente, senha, destinatario, assunto, corpo, anexos):

    mensagem = MIMEMultipart("mixed")
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    mensagem.attach(MIMEText(corpo, "plain"))

    try:
        for anexo in anexos:
            buffer = anexo["buffer"]
            nome_arquivo = anexo["nome_arquivo"]
            tipo = anexo["tipo"]

            dados = buffer.getvalue()

            if tipo == "imagem":
                arquivo = MIMEImage(dados, _subtype="png")

            elif tipo == "pdf":
                arquivo = MIMEApplication(dados, _subtype="pdf")

            elif tipo == "txt":
                arquivo = MIMEApplication(dados, _subtype="txt")

            else:
                st.error("Tipo de anexo inválido.")
                return False

            arquivo.add_header(
                "Content-Disposition",
                "attachment",
                filename=nome_arquivo
            )

            mensagem.attach(arquivo)

    except Exception as e:
        st.error(f"Erro ao preparar os anexos: {e}")
        return False

    server = None

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(mensagem)

        return True

    except Exception as e:
        st.error(f"Erro ao enviar o e-mail: {e}")
        return False

    finally:
        if server:
            server.quit()