from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models import FileModel

class FileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_file(self, file_model: FileModel):
        self.db.add(file_model)
        await self.db.commit()
        await self.db.refresh(file_model)
        return file_model

    async def get_similar_files(self, query_embedding, top_k):
        query_sql = text(f"""
        SELECT id, filename, extracted_text, l2_distance(embedding, ARRAY[{','.join(map(str, query_embedding))}]::vector) AS similarity
        FROM files
        ORDER BY embedding <-> ARRAY[{','.join(map(str, query_embedding))}]::vector
        LIMIT :top_k;
        """)
        result = await self.db.execute(query_sql, {"top_k": top_k})
        return result.fetchall()
