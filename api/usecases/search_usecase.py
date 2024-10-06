import struct
from fastapi import HTTPException

from repositories.file_repository import FileRepository
from services.result_processing_service import process_search_results
from services.embedding_service import create_embedding
from framework.utils.byte_conversion_utils import float_list_to_bytes

async def search_similar_files_usecase(query: str, top_k: int, db):
    """
    Searches for files similar to the query based on embeddings.
    Args:
        query (str): The query to search.
        top_k (int): The number of top similar files to return.
        db (AsyncSession): The database session.
    Returns:
        list: A list of files similar to the query.
    """
    embedding_vector = await create_embedding(query)
    vector_bytes = float_list_to_bytes(embedding_vector)
    float_list = struct.unpack('f' * (len(vector_bytes) // 4), vector_bytes)

    repo = FileRepository(db)
    results = await repo.get_similar_files(float_list, top_k)

    if not results:
        raise HTTPException(status_code=404, detail="No similar files found.")

    return await process_search_results(results, embedding_vector, top_k)
