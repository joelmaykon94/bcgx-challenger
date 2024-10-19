import streamlit as st
import requests
import os
from dotenv import load_dotenv

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
        if response.status_code == 200:
            return response.json()
        else:
            return {"answer": f"Error: Received response with status code {response.status_code}"}
    except requests.exceptions.HTTPError as http_err:
        return {"answer": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"answer": f"An error occurred: {err}"}

st.title('Chatbot BCGX Challenge 2024')

if 'upload_in_progress' not in st.session_state:
    st.session_state.upload_in_progress = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

file = st.file_uploader("Faça o upload de um documento PDF", type=["pdf", "txt"])

if st.session_state.upload_in_progress:
    st.warning("Aguarde, o upload está em progresso...")
    st.stop()

if st.button("Fazer upload") and file:
    st.session_state.upload_in_progress = True
    st.session_state.chat_history.append({"assistant": "Ok, vamos fazer o upload do seu documento."})
    
    with st.spinner('Aguarde enquanto o arquivo está sendo processado...'):
        file.seek(0)
        data = upload_file(file)
        message = data.get('response', {}).get('message', "")
        filename = data.get('response', {}).get('filename', "")
        
        if message:
            st.success(f"{message}: {filename}")
            st.session_state.chat_history.append({"assistant": f"Documento '{filename}' salvo com sucesso!"})
        else:
            st.session_state.chat_history.append({"assistant": "Falha ao salvar o documento. Tente novamente."})

    st.session_state.upload_in_progress = False

for entry in st.session_state.chat_history:
    if 'user' in entry:
        st.markdown(f"**Gestor:** {entry['user']}")
    if 'assistant' in entry:
        st.markdown(f"**Assistente:** {entry['assistant']}")

user_input = st.text_input("Digite sua questão ou texto aqui:", value=st.session_state.user_input, key="input_box")

if st.session_state.upload_in_progress:
    st.text_input("Digite sua questão ou texto aqui:", value=user_input, key="input_box", disabled=True)
    send_button_disabled = True
else:
    send_button_disabled = False

if st.button("Enviar pergunta", key="send_button", disabled=send_button_disabled):
    if user_input:
        st.session_state.chat_history.append({"user": user_input})
        st.session_state.upload_in_progress = True  # Disable further inputs during API call
        data = get_qna(user_input)

        if data["answer"]:
            st.session_state.chat_history.append({"assistant": data["answer"]})
        else:
            st.session_state.chat_history.append({"assistant": "Erro ao buscar resposta."})

        st.session_state.user_input = ""
        st.session_state.upload_in_progress = False

if st.button("Limpar histórico"):
    st.session_state.chat_history = []
