import re
from services.embedding_service import create_embedding_batch
from framework.utils.math_utils import l2_distance

async def process_search_results(results, embedding_vector, top_k):
    """
    Processes search results to include similarity scores and top phrases.
    Args:
        results (list): List of file results from the database.
        embedding_vector (list): The embedding vector of the search query.
        top_k (int): The number of top results to process.
    Returns:
        list: A list of processed results with similarity scores.
    """
    return [
        {
            "id": row.id,
            "filename": row.filename,
            "similarity_score": round(1 - row.similarity, 3),
            "top_phrases": await get_top_phrases(row.extracted_text, embedding_vector, top_k),
        }
        for row in results
    ]

async def get_top_phrases(extracted_text, query_embedding, top_k):
    """
    Retrieves top phrases from the text based on similarity to the query.
    Args:
        extracted_text (str): The extracted text from the file.
        query_embedding (list): The embedding of the query.
        top_k (int): Number of top phrases to return.
    Returns:
        list: List of top phrases with scores.
    """
    phrases = re.split(r'(?<=[.!?]) +', extracted_text.strip())
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]
    phrase_embeddings = await create_embedding_batch(phrases)

    phrase_scores = []
    for phrase, phrase_embedding in zip(phrases, phrase_embeddings):
        distance = l2_distance(query_embedding, phrase_embedding)
        score = round(1 - distance, 3)
        phrase_scores.append({"phrase": phrase, "score": score})

    phrase_scores.sort(key=lambda x: x["score"], reverse=True)
    return phrase_scores[:top_k]
