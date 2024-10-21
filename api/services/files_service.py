import io

from langchain import LLMChain
from langchain.chains import RetrievalQA, StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               PromptTemplate)
from langchain.schema import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.partition.pdf import partition_pdf
from utils.clean_text import clean_pdf


class FilesService:
    @staticmethod
    def _openai_streamer(retr_qa: RetrievalQA, text: str):
        for resp in retr_qa.run(text):
            yield resp

    @staticmethod
    async def query(question, temperature, n_docs, vectorstore):
        llm = ChatOpenAI(model_name="gpt-4o", streaming=True,
                         temperature=temperature)

        messages = [
            SystemMessage(
                content="Você é um algoritmo de classe mundial para responder perguntas com base em documentos."
            ),
            HumanMessage(
                content="Use como base as informações contidas nos documentos para responder à pergunta:"
            ),
            HumanMessagePromptTemplate.from_template("{context}"),
            HumanMessage(
                content="Dicas: Se você não encontrar uma resposta relevante nos documentos fornecidos, diga que não sabe e não irá poder ajudar."
            ),
            HumanMessage(
                content="Dicas: Se encontrar a resposta relevante nos documentos fornecidos, cite as referências e qual documento do banco de dados foi utilizado. Exemplo: 'O primeiro documento contém determinada informação que...'"
            ),
            HumanMessagePromptTemplate.from_template("Pergunta: {question}"),
            HumanMessagePromptTemplate.from_template("Dicas: Se encontrar a resposta relevante nos documentos fornecidos, complemente com um resumo do comportamento ideal para que a solução seja efetiva para a gestão pública para a seguinte questão: {question}"),
        ]

        prompt = ChatPromptTemplate(messages=messages)

        qa_chain = LLMChain(llm=llm, prompt=prompt)

        doc_prompt = PromptTemplate(
            template="Conteúdo do Documento: {page_content}",
            input_variables=["page_content"],
        )

        final_qa_chain = StuffDocumentsChain(
            llm_chain=qa_chain,
            document_variable_name="context",
            document_prompt=doc_prompt,
        )

        retrieval_qa = RetrievalQA(
            retriever=vectorstore.as_retriever(search_kwargs={"k": n_docs}),
            combine_documents_chain=final_qa_chain,
        )

        return FilesService._openai_streamer(retrieval_qa, question)

    @staticmethod
    async def upload(file, chunk_size, vectorstore):
        response = {}
        existing_doc = await vectorstore.get_document_by_filename(file.filename)
        if not existing_doc:
            data = await file.read()
            elements = partition_pdf(file=io.BytesIO(data))

            text = [clean_pdf(ele.text) for ele in elements if ele.text]

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=20,
                length_function=len,
                add_start_index=True,
            )

            docs = text_splitter.create_documents(text)

            for doc in docs:
                doc.metadata = {
                    "document_name": file.filename,
                    "title": file.filename.split('.')[0]
                }

            vectorstore.add_documents(docs)

            response = {
                'message': 'Arquivo carregado com sucesso',
                'filename': file.filename,
                'extracted_text': docs[0].page_content if docs else 'Texto não disponível',
                'embedding_size': len(docs) if docs else 'Tamanho não disponível'
            }
            return response

        response = {
                'message': 'Arquivo já existe no banco de dados',
                'filename': file.filename,
                'extracted_text': docs[0].page_content if docs else 'Texto não disponível',
                'embedding_size': len(docs) if docs else 'Tamanho não disponível'
            }
        return response

            