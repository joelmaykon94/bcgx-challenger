import asyncio
from io import BytesIO
import os
import struct
import re
from fastapi import HTTPException
from framework.pdf_utils import extract_text_from_pdf
from framework.database import SessionLocal
from repositories.file_repository import FileRepository
from openai import OpenAI
from domain.models import FileModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def upload_file(document):
    file_content = BytesIO()
    while chunk := await document.read(1024):
        file_content.write(chunk)

    content = file_content.getvalue()
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    text = extract_text_from_pdf(content)
    embedding_vector = await create_embedding(text)

    async with SessionLocal() as db:
        repo = FileRepository(db)
        file_entry = FileModel(
            filename=document.filename,
            content=content,
            extracted_text=text,
            embedding=embedding_vector
        )
        return await repo.add_file(file_entry)

async def search_similar_files(query: str, top_k: int):
    embedding_vector = await create_embedding(query)
    vector_bytes = float_list_to_bytes(embedding_vector)
    float_list = struct.unpack('f' * (len(vector_bytes) // 4), vector_bytes)

    async with SessionLocal() as db:
        repo = FileRepository(db)
        results = await repo.get_similar_files(float_list, top_k)
        
        if not results:
            raise HTTPException(status_code=404, detail="No similar files found.")
        
        return await process_results(results, embedding_vector, top_k)

async def process_results(results, embedding_vector, top_k):
    return [
        {
            "id": row.id,
            "filename": row.filename,
            "similarity_score": round(1 - row.similarity, 3),
            "top_phrases": await get_top_phrases(
                row.extracted_text, embedding_vector, top_k
            ),
        }
        for row in results
    ]


async def get_top_phrases(extracted_text, query_embedding, top_k):
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

async def create_embedding(query: str):
    response = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
    )
    
    return response.data[0].embedding


async def create_embedding_batch(phrases):
    if not phrases:
        return []
    
    loop = asyncio.get_event_loop()

    try:
        response = await loop.run_in_executor(
            None,
            lambda: client.embeddings.create(
                model="text-embedding-ada-002",
                input=phrases
            )
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        raise RuntimeError(f"Error creating batch embeddings: {str(e)}") from e

def float_list_to_bytes(float_list):
    return struct.pack('f' * len(float_list), *float_list)

def l2_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
