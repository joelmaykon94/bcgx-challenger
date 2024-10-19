import streamlit as st
from domain.services.query_service import QueryService
from domain.services.upload_service import UploadService


from interfaces.upload_interface import handle_upload
from interfaces.query_interface import handle_submit

st.set_page_config(page_title="💬 EcoBot A.I")

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>EcoBot A.I</h1>
    <h2 style='text-align: center; color: #555;'>Seu Assistente inteligente de pesquisa em documentos. </h2>
    <p style='text-align: center; color: #555;'> © BCGX Challenge 2024 </p>
    """,
    unsafe_allow_html=True,
)

if "upload_in_progress" not in st.session_state:
    st.session_state.upload_in_progress = False

upload_instruction = (
    "Arraste e solte o arquivo aqui ou clique para selecionar um arquivo PDF ou TXT."
)
upload_limit = "O tamanho máximo do arquivo permitido é de 10 MB."

with st.form(key="upload_form"):
    file = st.file_uploader(
        label=upload_instruction, type=["pdf", "txt"], label_visibility="visible"
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
                f"<span style='color: #4CAF50;'> {message['content']}</span>"
            )
            st.markdown(answer_assistant, unsafe_allow_html=True)
    else:
        with st.chat_message("user"):
            question_user = (
                f"<span style='color: #007BFF;'> {message['content']}</span>"
            )
            st.markdown(question_user, unsafe_allow_html=True)

if prompt := st.chat_input(placeholder="Digite sua mensagem aqui"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        question_user = f"<span style='color: #007BFF;'> {prompt}</span>"
        st.markdown(question_user, unsafe_allow_html=True)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = QueryService.get_qna(prompt)
            answer = f"<span style='color: #4CAF50;'> {response.answer}</span>"
            st.markdown(answer, unsafe_allow_html=True)
        message = {"role": "assistant", "content": response.answer}
        st.session_state.messages.append(message)

if st.checkbox("ver resultados da sessão"):
    st.write(st.session_state)
