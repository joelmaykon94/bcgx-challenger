from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models import FileModel

class FileRepository:
    """
    A repository class for managing file-related operations in the database.

    Attributes:
        db (AsyncSession): The asynchronous session object used to interact with the database.
    """
    def __init__(self, db: AsyncSession):
        """
        Initializes the FileRepository with a database session.

        Args:
            db (AsyncSession): An asynchronous database session used for database operations.
        """
        self.db = db

    async def add_file(self, file_model: FileModel):
        """
        Adds a new file to the database.

        Args:
            file_model (FileModel): An instance of FileModel representing the file to be added.

        Returns:
            FileModel: The file model that was added to the database, refreshed with updated state (e.g., primary key).
        """
        self.db.add(file_model)
        await self.db.commit()
        await self.db.refresh(file_model)
        return file_model

    async def get_similar_files(self, query_embedding, top_k):
        """
        Retrieves files from the database that are most similar to the given embedding vector.

        Args:
            query_embedding (list of float): The embedding vector to compare against files in the database.
            top_k (int): The number of top similar files to return.

        Returns:
            list: A list of files (id, filename, extracted_text, similarity score) ordered by similarity to the query embedding.
        """
        query_sql = text(f"""
        SELECT id, filename, extracted_text, l2_distance(embedding, ARRAY[{','.join(map(str, query_embedding))}]::vector) AS similarity
        FROM files
        ORDER BY embedding <-> ARRAY[{','.join(map(str, query_embedding))}]::vector
        LIMIT :top_k;
        """)
        result = await self.db.execute(query_sql, {"top_k": top_k})
        return result.fetchall()
