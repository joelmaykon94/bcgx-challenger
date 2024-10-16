from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.file_repository import FileRepository
from services.embedding_service import create_embedding
from services.ragas_services import evaluate_answer_metrics
from repositories.file_repository import FileRepository
from services.result_processing_service import process_search_results
async def process_question_answer(question: str, top_k: int, db: AsyncSession):
    query_embedding = await create_embedding(question)

    await db.begin()
    try:
        repo = FileRepository(db)
        results = await repo.get_similar_files(query_embedding, top_k)

    except Exception as e:
        raise HTTPException(status_code=404, detail="No similar files found.") from e

    documents = await process_search_results(results, query_embedding, top_k)
    score = await evaluate_answer_metrics(question, documents)
    print(score)
    return {"documents": documents, "relevancy_score": score}
