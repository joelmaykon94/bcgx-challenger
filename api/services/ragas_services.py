import os
from ragas.metrics import AnswerRelevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from ragas.dataset_schema import SingleTurnSample

# Initialize the Language Model and Embeddings Wrappers using OpenAI API
llm = LangchainLLMWrapper(ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY")))
emb = LangchainEmbeddingsWrapper(OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")))

# Instantiate the Answer Relevancy metric with the LLM and Embeddings
answer_relevancy_metric = AnswerRelevancy(llm=llm, embeddings=emb)

async def evaluate_answer_relevancy(question, response_data):
    """
    Evaluates the relevancy of an answer to a given question using a pre-defined metric.

    Args:
        question (str): The user-input question to be evaluated.
        response_data (dict): A dictionary containing the response and retrieved contexts.
            - response_data['response'] (str): The generated response to be evaluated.
            - response_data['retrieved_contexts'] (list of dict): Contextual information that was used to generate the response.

    Returns:
        float: A score representing the relevancy of the answer to the given question.

    Example:
        response_data = {
            "response": "This is the generated response.",
            "retrieved_contexts": [{"extracted_text": "Context related to the question."}]
        }
        score = await evaluate_answer_relevancy("What is the capital of France?", response_data)
    """
    row = SingleTurnSample(user_input=question, response=response_data["response"], retrieved_contexts=[context["extracted_text"] for context in response_data])

    async def get_score(metric, row):
        """
        Helper function to calculate the relevancy score for a given row.

        Args:
            metric (AnswerRelevancy): The metric used to calculate the score.
            row (SingleTurnSample): The sample containing the question, response, and contexts.

        Returns:
            float: The relevancy score for the sample.
        """
        score = await metric.single_turn_ascore(row)
        return score

    return await get_score(answer_relevancy_metric, row)
