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
        response_data (list): A list containing dictionaries with the response and retrieved contexts.
            - response_data[0]['top_phrases'] (list of dict): Contextual information that was used to generate the response.

    Returns:
        float: A score representing the relevancy of the answer to the given question.

    Example:
        response_data = [
            {
                "id": 1,
                "filename": "document.pdf",
                "similarity_score": 0.312,
                "top_phrases": [
                    {"phrase": "Sample phrase 1", "score": 0.442},
                    {"phrase": "Sample phrase 2", "score": 0.431},
                    # more phrases...
                ]
            }
        ]
        score = await evaluate_answer_relevancy("What is the capital of France?", response_data)
    """
    try:
        top_phrases = response_data[0]["top_phrases"]
        retrieved_contexts = [context["phrase"] for context in top_phrases]
        row = SingleTurnSample(user_input=question, response=top_phrases[0]["phrase"], retrieved_contexts=retrieved_contexts)

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

    except KeyError as e:
        raise ValueError(f"Key error: {str(e)}. Ensure 'top_phrases' is present in response_data.") from e

    except IndexError as e:
        raise ValueError("Index error: response_data is empty or does not contain the expected structure.") from e

    except TypeError as e:
        raise ValueError(f"Type error: {str(e)}. Please check the structure of response_data.") from e

    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {str(e)}") from e
