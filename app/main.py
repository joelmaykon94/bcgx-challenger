import streamlit as st
from core.services.query_service import QueryService
from core.services.upload_service import UploadService

st.set_page_config(page_title="Eco Docs A.I",  page_icon="🤖")

st.markdown(
    """
    <style>
    div.stApp {
        background: radial-gradient(circle, #a8e6cf, #dcedc1);
        font-family: Arial, sans-serif;
        color: #333333;  /* Cor escura para o texto */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 1000;
        text-align: center;
        padding: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .fixed-header img {
        margin-top: 3%;
        max-width: 80px; /* Tamanho ajustado da imagem */
        height: auto;
    }
    
    .stApp {
        margin-top: 10%;
    }
    </style>
    
    <div class="fixed-header">
        <img src="https://attic.sh/i79ivnxsy801bk07vu6qp0ho1pmm" alt="Logo" />
        <h4 style='color: #4CAF50;'>EcoDocs A.I</h4>
        <p style='color: #555;'>© BCGX Challenge 2024</p>
    </div>
    """,
    unsafe_allow_html=True,
)


if "upload_in_progress" not in st.session_state:
    st.session_state.upload_in_progress = False

upload_instruction = (
    "Arraste e solte o arquivo aqui ou clique para selecionar um arquivo PDF."
)
upload_limit = "O tamanho máximo do arquivo permitido é de 200 MB."

with st.form(key="upload_form"):
    file = st.file_uploader(
        label=upload_instruction, type=["pdf"], label_visibility="visible"
    )
    st.write(upload_limit)
    submit_upload = st.form_submit_button(label="Fazer upload")

    if submit_upload and file:
        st.session_state.upload_in_progress = True
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": "Ok, vamos fazer o upload do seu documento.",
            }
        )

        with st.spinner("Aguarde enquanto o arquivo está sendo processado..."):
            file.seek(0)
            upload_response = UploadService.upload_file(file)
            if upload_response.message:
                message_filename = (
                    f"{upload_response.message}: {upload_response.filename}"
                )
                st.success(message_filename)
                message_success = {
                    "role": "assistant",
                    "content": f"Documento '{ upload_response.filename}' salvo com sucesso!",
                }
                st.session_state.messages.append(message_success)
            else:
                message_failed = {
                    "role": "assistant",
                    "content": "Falha ao salvar o documento. Tente novamente.",
                }
                st.session_state.messages.append(message_failed)

        st.session_state.upload_in_progress = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Oi, como posso te ajudar?"}
    ]

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            answer_assistant = (
                f"<span style='color: #333333; font-size: 18px; font-family: Arial, sans-serif;'>"
                f" {message['content']}</span>"
            )
            st.markdown(answer_assistant, unsafe_allow_html=True)
    else:
        with st.chat_message("user"):
            question_user = (
                f"<span style='color: #000000; font-size: 18px; font-family: Arial, sans-serif;'>"
                f" {message['content']}</span>"
            )
            st.markdown(question_user, unsafe_allow_html=True)

if prompt := st.chat_input(placeholder="Digite sua mensagem aqui"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        question_user = f"<span style='color: #000000; font-size: 18px; font-family: Arial, sans-serif;'> {prompt}</span>"
        st.markdown(question_user, unsafe_allow_html=True)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = QueryService.get_qna(prompt)
            answer = f"<span style='color: #333333; font-size: 18px; font-family: Arial, sans-serif;'> {response.answer}</span>"
            st.markdown(answer, unsafe_allow_html=True)
        message = {"role": "assistant", "content": response.answer}
        st.session_state.messages.append(message)


if st.checkbox("ver resultados da sessão"):
    st.write(st.session_state)
