from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from weaviate.embedded import EmbeddedOptions
from dotenv import load_dotenv, find_dotenv
from langchain_core.documents import Document


client = weaviate.Client(
    embedded_options=EmbeddedOptions()
)

def create_vectorstore_from_documents(documents):
    embeddings = OpenAIEmbeddings()

    vectorstore = Weaviate.from_documents(
        client=client,
        documents=documents,
        embedding=embeddings,
        by_text=False
    )

    return vectorstore

def initialize_retriever(documents):
    vectorstore = create_vectorstore_from_documents(documents)
    retriever = vectorstore.as_retriever()
    
    return retriever


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use two sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

metrics = [faithfulness]

async def get_answers_from_questions(questions, documents):
    retriever = initialize_retriever(documents)

    rag_chain = (
        {"context": retriever,  "question": RunnablePassthrough()} 
        | prompt 
        | llm
        | StrOutputParser() 
    )
    
    answers = []
    contexts = []

    for query in questions:
        answer = rag_chain.invoke(query)
        contexts.append([docs.page_content for docs in retriever.get_relevant_documents(query)])
        answers.append(answer)

    return answers, contexts

async def evaluate_answer_metrics(question, documents):
    """
    Avalia a resposta utilizando múltiplas métricas predefinidas.

    Args:
        question (str): Pergunta do usuário.
        documents (list): Lista contendo os dados de resposta e contextos recuperados.

    Returns:
        dict: Resultados das métricas para a pergunta fornecida.
    """
    if not documents or "top_phrases" not in documents[0]:
        raise ValueError(
            "A estrutura de documents é inválida. A chave 'top_phrases' está faltando.")
    
    retrieved_contexts = [
        Document(
            page_content=phrase["phrase"],
        )
        for document in documents 
        for phrase in document["top_phrases"]  
    
    questions = [question]
    answers, contexts = await get_answers_from_questions(questions=questions, documents=retrieved_contexts) 

    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
    })
    print(dataset)
    return evaluate(dataset=dataset, metrics=metrics)