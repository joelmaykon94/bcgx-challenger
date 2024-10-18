import streamlit as st
import requests
import simplejson as json
import os
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()

api = os.getenv("API_URL")

def upload_file(file):
    url = f"{api}/files/upload"

    try:
        files = {'file': file}
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"answer": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"answer": f"An error occurred: {err}"}

def get_qna(question):
    url = f"{api}/files/query"
    params = {
        "question": question,
        "temperature": 0.6,
        "n_docs": 3
    }

    try:
        response = requests.get(url, params=params)  
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

    for entry in chat_history:
        if 'user' in entry:
            pdf.cell(200, 10, txt=f"Gestor: {entry['user']}", ln=True)
        if 'assistant' in entry:
            pdf.cell(200, 10, txt=f"Assistente: {entry['assistant']}", ln=True)
    
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

st.title('Chatbot BCGX Challenge 2024')

if 'upload_in_progress' not in st.session_state:
    st.session_state.upload_in_progress = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with st.container():
    file = st.file_uploader("Faça o upload de um PDF ou TXT", type=["pdf", "txt"])

    if st.button("Fazer upload", key="upload_button", disabled=st.session_state.upload_in_progress) and file:
        st.session_state.upload_in_progress = True
        with st.spinner('Aguarde enquanto o arquivo está sendo processado...'):
            file.seek(0)
            response = upload_file(file)

            if 'message' in response:
                st.success(f"{response['message']}: {response['filename']}")
                st.session_state.chat_history.append({"assistant": f"Documento '{response['filename']}' salvo com sucesso!"})
            else:
                st.error('Falha no envio do arquivo. Tente novamente ou entre em contato com o suporte.')
                st.session_state.chat_history.append({"assistant": "Falha ao salvar o documento. Tente novamente ou entre em contato com o suporte."})

        st.session_state.upload_in_progress = False  # Marca o fim do upload

for entry in st.session_state.chat_history:
    if 'user' in entry:
        st.markdown(f"**Gestor:** {entry['user']}")
    if 'assistant' in entry:
        st.markdown(f"**Assistente:** {entry['assistant']}")

user_input = st.text_input("Digite sua questão ou texto aqui:", key="input_box", help="Digite aqui sua pergunta para o assistente")

if st.button("Enviar pergunta", key="send_button"):
    if user_input:
        st.session_state.chat_history.append({"user": user_input})
        response = get_qna(user_input)

        if "answer" in response:
            st.session_state.chat_history.append({"assistant": response['answer']})
        else:
            st.session_state.chat_history.append({"assistant": "Error fetching answer."})

        st.experimental_rerun()

if st.session_state.chat_history:
    pdf_data = gerar_pdf(st.session_state.chat_history)
    st.download_button(
        "Exportar diálogo em PDF",
        data=pdf_data,
        file_name="chat_gestor.pdf",
        mime="application/pdf",
    )

if st.button("Limpar histórico", key="clear_button"):
    st.session_state.chat_history = []
    st.experimental_rerun()
