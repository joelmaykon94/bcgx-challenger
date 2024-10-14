import streamlit as st
import requests
import simplejson as json
import os
from dotenv import load_dotenv
import time  # Certifique-se de importar o módulo time
from fpdf import FPDF

load_dotenv()

api = os.getenv("API_URL")

def upload_pdf(file):
    url = f"{api}/upload_file"  # Endpoint correto para o upload do PDF

    try:
        # Abrir o arquivo como binário para enviá-lo
        files = {'document': file}  # 'document' deve corresponder ao parâmetro da API
        response = requests.post(url, files=files)
        response.raise_for_status()  # Levanta erro para códigos 4xx/5xx
        return response.json()  # Supondo que a API retorna a resposta em formato JSON
    except requests.exceptions.HTTPError as http_err:
        return {"answer": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"answer": f"An error occurred: {err}"}

def get_qna(question):
    url = f"{api}/qna?question={question}"  # URL para perguntas e respostas
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"answer": f"HTTP error occurred: {http_err}", "references": []}
    except Exception as err:
        return {"answer": f"An error occurred: {err}", "references": []}

def gerar_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Adiciona cada entrada do chat no PDF
    for entry in chat_history:
        if 'user' in entry:
            pdf.cell(200, 10, txt=f"Gestor: {entry['user']}", ln=True)
        if 'assistant' in entry:
            pdf.cell(200, 10, txt=f"Assistente: {entry['assistant']}", ln=True)
    
    # Gera o PDF em um buffer de memória
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

def get_pdf_list():
    try:
        response = requests.get(f"{api}/list_pdfs")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar lista de PDFs: {e}")
        return []

def open_pdf_modal():
    st.subheader("Lista de PDFs")
    pdf_files = get_pdf_list()

    if pdf_files:
        for pdf in pdf_files:
            pdf_link = f"{api}/get_pdf/{pdf['filename']}"
            st.markdown(f"[Abrir {pdf['filename']}]({pdf_link})", unsafe_allow_html=True)
    else:
        st.write("Nenhum arquivo PDF encontrado.")

with st.sidebar:
    st.subheader('Chatbot BCGX Challenge 2024')

    st.divider()

    btns = st.container()

    # Uploader para PDF
    file = st.file_uploader("Upload de PDF", type=["pdf"])

    # Botão para fazer o upload do PDF
    if st.button("Fazer upload", key="upload_button") and file:
        # Chamada à API para upload do PDF sem barra de progresso
        with st.spinner('Aguarde enquanto o arquivo está sendo processado...'):
            file.seek(0)  # Reposiciona o ponteiro do arquivo no início
            response = upload_pdf(file)

            if 'message' in response:
                st.success(f"{response['message']}: {response['filename']}")
                st.write(f"Texto extraído (primeiros 100 caracteres): {response['extracted_text']}")
                st.write(f"Tamanho do embedding: {response['embedding_size']}")
            else:
                st.error('Falha no envio do arquivo. Tente novamente.')
    
    if st.button("Ver PDFs Disponíveis"):
        open_pdf_modal()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if query := st.chat_input('Digite sua questão aqui'):
    st.session_state.chat_history.append({"user": query})  # Add user query to chat history

    response = get_qna(query)
    
    if "answer" in response:
        st.session_state.chat_history.append({"assistant": response['answer']})
    else:
        st.session_state.chat_history.append({"assistant": "Error fetching answer."})

    for entry in st.session_state.chat_history:
        if 'user' in entry:
            st.markdown(f"**Gestor:** {entry['user']}")
        if 'assistant' in entry:
            st.markdown(f"**Assistente:** {entry['assistant']}")

if st.session_state.chat_history:
    pdf_data = gerar_pdf(st.session_state.chat_history)
    btns.download_button(
        "Exportar diálogo em PDF",
        data=pdf_data,
        file_name="chat_gestor.pdf",
        mime="application/pdf",
    )


# Corrigido: Adicionado `key` único ao botão "Limpar histórico"
if btns.button("Limpar histórico", key="clear_button"):
    st.session_state.chat_history = []
