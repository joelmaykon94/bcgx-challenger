from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector # type: ignore

Base = declarative_base()

class FileModel(Base):
    """
    Database model representing a file.

    Attributes:
        id (Integer): Unique identifier for each file.
        filename (String): Name of the file.
        content (LargeBinary): Binary content of the file (e.g., the file itself).
        extracted_text (String): Text extracted from the file for further processing.
        embedding (Vector): Vector representation of the file's content, used for similarity search or other tasks.
    """
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(LargeBinary) 
    extracted_text = Column(String)
    embedding = Column(Vector(1536))
