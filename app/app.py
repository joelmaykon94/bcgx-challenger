import streamlit as st
import requests
import simplejson as json
import os
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("API_URL")

def get_qna(question):
    url = f"{api}/qna?question={question}"
    try:
        response = requests.get(url)
        print(response)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"answer": f"HTTP error occurred: {http_err}", "references": []}
    except Exception as err:
        return {"answer": f"An error occurred: {err}", "references": []}

with st.sidebar:
    st.subheader('Chatbot BCGX Challenge 2024')

    st.divider()

    btns = st.container()

    file = st.file_uploader("Upload de PDF", type=["pdf"])

    if st.button("Fazer upload") and file:
        data = json.load(file)
        st.session_state.chat_history = data

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
            st.markdown(f"**Servidor:** {entry['user']}")
        if 'assistant' in entry:
            st.markdown(f"**Assistente:** {entry['assistant']}")

# Optional buttons for multimedia
#cols = st.columns(2)
#if cols[0].button('Show me the multimedia'):
#   st.image('https://tse4-mm.cn.bing.net/th/id/OIP-C.cy76ifbr2oQPMEs2H82D-QHaEv?w=284&h=181&c=7&r=0&o=5&dpr=1.5&pid=1.7')
#   time.sleep(0.5)
#   st.video('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4')
#   time.sleep(0.5)
#   st.audio('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4')

btns.download_button(
    "Exportar Markdown",
    "".join(f"**Servidor:** {entry.get('user', '')}\n**Assistente:** {entry.get('assistant', '')}\n" for entry in st.session_state.chat_history),
    file_name="chat_history.md",
    mime="text/markdown",
)

btns.download_button(
    "Exportar JSON",
    json.dumps(st.session_state.chat_history),
    file_name="chat_history.json",
    mime="text/json",
)

if btns.button("Limpar histórico"):
    st.session_state.chat_history = []
