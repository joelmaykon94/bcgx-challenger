import io
import os

from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import AnswerRelevancy
from ragas.metrics import LLMContextPrecisionWithoutReference
from ragas.dataset_schema import SingleTurnSample

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain import LLMChain
from langchain.chains import RetrievalQA, StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
)

from datasets import Dataset
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from langchain.schema import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.partition.pdf import partition_pdf

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

"""
#ragas evaluate - execution is slow

retriever = vectorstore.as_retriever(search_kwargs={"k": n_docs})

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        questions = [
            "Como podemos identificar as vulnerabilidades climáticas específicas do nosso município?",
            "Quais são as principais fontes de dados climáticos confiáveis para nossa região?",
            "É possível gerar relatórios personalizados sobre riscos climáticos para nosso município?",
            "Como lidar com informações conflitantes entre diferentes documentos sobre mudanças climáticas?",
            "Qual é a precisão das previsões climáticas disponíveis para nossa área?",
            "Que medidas de adaptação são mais adequadas para nossa região específica?",
            "Como priorizar as ações de adaptação recomendadas?",
            "Onde posso encontrar estimativas de custos para as medidas de adaptação sugeridas?",
            "Como integrar dados locais com informações nacionais e globais sobre mudanças climáticas?",
            "Quais são os limites éticos e legais na tomada de decisões municipais relacionadas à adaptação climática?",
            "Quais são as possíveis fontes de financiamento para projetos de adaptação climática?",
            "Como lidar com incertezas nas projeções climáticas de longo prazo em nosso planejamento?",
            "Que elementos devem ser incluídos em planos de contingência para eventos climáticos extremos?",
            "Como considerar as especificidades socioeconômicas do município nas estratégias de adaptação?",
            "Qual o impacto potencial das mudanças climáticas nos diferentes setores econômicos do nosso município?",
            "Quais são as melhores práticas para comunicar riscos climáticos à população?",
            "Existem exemplos de adaptação climática bem-sucedida em municípios similares ao nosso?",
            "Como integrar considerações sobre justiça climática em nosso plano de adaptação?",
            "Quais são as possíveis sinergias entre medidas de adaptação e mitigação climática?",
            "Como manter-se atualizado sobre mudanças em políticas e regulamentações climáticas?",
            "Quais critérios devemos usar para definir metas de adaptação climática para o município?",
            "Como avaliar e melhorar a capacidade adaptativa local?",
            "Existem oportunidades de parcerias público-privadas para adaptação climática em nosso município?",
            "Como abordar questões de segurança alimentar no contexto das mudanças climáticas?",
            "Que métodos podemos usar para realizar análises de custo-benefício de diferentes estratégias de adaptação?",
            "Como integrar a adaptação climática em outros planos municipais existentes?",
            "Qual a importância de considerar projeções demográficas nas estratégias de adaptação?",
            "Quais são os principais impactos das mudanças climáticas na saúde pública local?",
            "Como identificar e resolver potenciais conflitos entre diferentes estratégias de adaptação?",
            "Que medidas podem ser tomadas para preservar o patrimônio cultural diante das mudanças climáticas?",
            "Como avaliar a eficácia de medidas de adaptação já implementadas?",
            "Quais são as principais preocupações na gestão de recursos hídricos frente às mudanças climáticas?",
            "Quais são as principais lacunas de conhecimento que precisamos preencher para melhorar nosso planejamento de adaptação?",
            "Como as mudanças climáticas afetam a biodiversidade local e o que podemos fazer a respeito?",
            "Quais são as melhores estratégias para engajar a comunidade no processo de adaptação climática?",
            "Como podemos melhorar a resiliência urbana em nosso município?",
            "Quais setores da nossa economia local são mais vulneráveis às mudanças climáticas?",
            "Como podemos incorporar tecnologias verdes em nosso plano de adaptação climática?",
            "Quais são os principais desafios na implementação de um plano de adaptação climática em um município como o nosso?",
            "Como podemos medir e monitorar o progresso de nossas iniciativas de adaptação climática ao longo do tempo?",
        ]

        ground_truths = [
            [
                "O relatório indica que as vulnerabilidades climáticas no município incluem áreas de baixa altitude sujeitas a inundações e setores agrícolas afetados pela seca."
            ],
            [
                "As principais fontes de dados climáticos confiáveis para a região incluem o Instituto Nacional de Meteorologia e o Centro de Monitoramento de Desastres Naturais."
            ],
            [
                "O sistema atual permite a geração de relatórios personalizados sobre riscos climáticos com base em dados locais e regionais, incluindo previsões de eventos extremos."
            ],
            [
                "Quando há informações conflitantes entre documentos sobre mudanças climáticas, recomenda-se priorizar estudos mais recentes e fontes governamentais."
            ],
            [
                "A precisão das previsões climáticas para a área é moderada, especialmente para projeções de longo prazo, que dependem de modelos climáticos regionais."
            ],
            [
                "As medidas de adaptação recomendadas para a região incluem a construção de reservatórios para armazenamento de água e a criação de áreas de conservação ambiental."
            ],
            [
                "Para priorizar ações de adaptação, recomenda-se considerar o impacto social, a viabilidade técnica e os custos associados a cada medida."
            ],
            [
                "Estimativas de custos para medidas de adaptação sugeridas podem ser encontradas em relatórios do Banco Mundial e da Agência de Proteção Ambiental."
            ],
            [
                "A integração de dados locais com informações nacionais e globais é feita através de plataformas de dados climáticos que conectam redes de monitoramento e sensores regionais."
            ],
            [
                "As decisões municipais relacionadas à adaptação climática devem respeitar os limites éticos e legais, assegurando que as ações não prejudiquem comunidades vulneráveis."
            ],
            [
                "Existem diversas fontes de financiamento para projetos de adaptação climática, incluindo fundos do governo federal e organizações internacionais."
            ],
            [
                "A incerteza nas projeções climáticas de longo prazo pode ser gerida utilizando múltiplos modelos de projeção e considerando cenários de risco."
            ],
            [
                "Os planos de contingência para eventos climáticos extremos devem incluir ações de evacuação, abrigos temporários e suporte médico emergencial."
            ],
            [
                "As estratégias de adaptação devem levar em conta as especificidades socioeconômicas locais, como a dependência da agricultura e o nível de desenvolvimento urbano."
            ],
            [
                "As mudanças climáticas têm impacto direto nos setores econômicos locais, especialmente agricultura, turismo e infraestrutura urbana."
            ],
            [
                "A comunicação eficaz dos riscos climáticos para a população deve ser clara e acessível, utilizando mídias locais e campanhas de conscientização."
            ],
            [
                "Exemplos de adaptação climática bem-sucedida incluem o uso de sistemas de irrigação eficiente em municípios com características agrícolas similares."
            ],
            [
                "A justiça climática deve ser considerada no plano de adaptação, garantindo que as políticas beneficiem igualmente todas as comunidades do município."
            ],
            [
                "Medidas de adaptação e mitigação climática podem ser sinérgicas, como o uso de energia renovável que reduz emissões e melhora a resiliência energética."
            ],
            [
                "Manter-se atualizado sobre mudanças em políticas e regulamentações climáticas é essencial para alinhar as ações municipais às diretrizes estaduais e federais."
            ],
            [
                "Critérios para definir metas de adaptação climática incluem viabilidade técnica, impacto social e sustentabilidade financeira das ações."
            ],
            [
                "A avaliação e melhoria da capacidade adaptativa local podem ser feitas através de investimentos em infraestrutura e programas de conscientização."
            ],
            [
                "Parcerias público-privadas são viáveis para adaptação climática, como em projetos de infraestrutura verde financiados em parte pelo setor privado."
            ],
            [
                "A segurança alimentar frente às mudanças climáticas pode ser abordada com políticas de apoio à agricultura local e incentivo a práticas sustentáveis."
            ],
            [
                "Análises de custo-benefício para estratégias de adaptação são feitas considerando o impacto econômico e social das medidas."
            ],
            [
                "A adaptação climática pode ser integrada a outros planos municipais existentes, como o plano diretor urbano e o plano de desenvolvimento sustentável."
            ],
            [
                "As projeções demográficas são importantes para estratégias de adaptação, pois mudanças populacionais influenciam a demanda por recursos e infraestrutura."
            ],
            [
                "As mudanças climáticas impactam a saúde pública local, com aumento de doenças respiratórias e problemas decorrentes de ondas de calor."
            ],
            [
                "Potenciais conflitos entre estratégias de adaptação podem ser resolvidos através de consultas públicas e avaliações de impacto ambiental."
            ],
            [
                "Medidas para preservar o patrimônio cultural diante das mudanças climáticas incluem a adaptação de edifícios históricos e a criação de áreas de preservação."
            ],
            [
                "A eficácia de medidas de adaptação pode ser avaliada com monitoramento contínuo e indicadores de desempenho específicos para cada ação."
            ],
            [
                "A gestão de recursos hídricos é essencial frente às mudanças climáticas, incluindo a proteção de nascentes e o uso eficiente de recursos hídricos."
            ],
            [
                "Lacunas de conhecimento sobre mudanças climáticas e adaptação podem ser preenchidas com pesquisa local e colaboração com instituições científicas."
            ],
            [
                "As mudanças climáticas afetam a biodiversidade local, podendo causar perda de espécies e alterações nos ecossistemas, o que demanda conservação de áreas naturais."
            ],
            [
                "Engajar a comunidade no processo de adaptação climática é essencial e pode ser feito através de programas de educação e participação cidadã."
            ],
            [
                "A resiliência urbana pode ser melhorada com infraestrutura adaptativa, como sistemas de drenagem eficientes e áreas verdes para controle de enchentes."
            ],
            [
                "Setores econômicos mais vulneráveis às mudanças climáticas incluem a agricultura e o turismo, que dependem de condições climáticas estáveis."
            ],
            [
                "A incorporação de tecnologias verdes no plano de adaptação climática inclui o uso de energia renovável e construção sustentável."
            ],
            [
                "Desafios na implementação de planos de adaptação em municípios incluem financiamento, capacidade técnica e aceitação da população local."
            ],
            [
                "O progresso de iniciativas de adaptação climática pode ser monitorado com indicadores de desempenho e relatórios periódicos de avaliação."
            ],
        ]

        answers = []
        contexts = []

        # Inference
        for query in questions:
            answers.append(rag_chain.invoke(query))
            contexts.append(
                [docs.page_content for docs in retriever.get_relevant_documents(query)]
            )
        # To dict
        data = {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truths": ground_truths,
            "reference":"plano de adaptação climática"
        }

        # Convert dict to dataset
        dataset = Dataset.from_dict(data)
        print(dataset)
        result = evaluate(
            dataset=dataset,
            metrics=[
                context_precision,
                context_recall,
                faithfulness,
                answer_relevancy,
            ],
        )

        print(result)
"""

from utils.clean_text import clean_pdf


class FilesService:
    @staticmethod
    def _openai_streamer(retr_qa: RetrievalQA, text: str):
        yield from retr_qa.run(text)

    @staticmethod
    async def query(question, temperature, n_docs, vectorstore):
        llm = ChatOpenAI(model_name="gpt-4o", streaming=True, temperature=temperature)

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
            HumanMessagePromptTemplate.from_template(
                "Dicas: Se encontrar a resposta com informações relevantes nos documentos similares fornecidos, complemente com um resumo do comportamento ideal para que a solução seja efetiva para a gestão pública para a seguinte questão: {question}"
            ),
            HumanMessagePromptTemplate.from_template(
                "Dicas: separe a resposta um titulo <b>🪴 Informações encontradas:</b> quebre em três linhas e outra parte que é o resumo do comportamento ideal para a solução em um título <b>💡 Solução efetiva sugerida:</b>"
            ),
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

        response = FilesService._openai_streamer(retrieval_qa, question)
        answers = []

        for item in response:
            answer = item.get("answer") if isinstance(item, dict) else str(item)
            if answer:
                answers.append(answer)

        return (
            "".join([str(answer) for answer in answers])
            if isinstance(answers, list)
            else str(answers)
        )

    @staticmethod
    async def upload(file, chunk_size, vectorstore):
        response = {}

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
                "title": file.filename.split(".")[0],
            }

        vectorstore.add_documents(docs)

        return {
            "message": "Arquivo carregado com sucesso",
            "filename": file.filename,
            "extracted_text": (
                docs[0].page_content if docs else "Texto não disponível"
            ),
            "embedding_size": len(docs) if docs else "Tamanho não disponível",
        }
