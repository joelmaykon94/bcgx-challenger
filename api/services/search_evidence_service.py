from langchain.vectorstores import Weaviate
import weaviate

# Conectar ao cliente do Weaviate
client = weaviate.Client("http://localhost:8080")

# Usar o Weaviate para criar um fluxo RAG que busca em documentos sobre SAI
def search_evidence(question):
    vectorstore = Weaviate(client, "Document", text_key="content")
    docs = vectorstore.similarity_search(question, k=3)
    
    return docs

# Exemplo de consulta
question = "Quais são os riscos de SAI para o clima?"
docs = search_evidence(question)

for doc in docs:
    print(f"Documento: {doc.metadata['document_name']}\nConteúdo: {doc.page_content}")
