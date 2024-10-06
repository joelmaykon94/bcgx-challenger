from fastapi import UploadFile, HTTPException
from services.embedding_service import process_text_and_generate_embeddings
from repositories.file_repository import FileRepository
from domain.models import FileModel

async def upload_file_usecase(document: UploadFile, db):
    """
    Handles the upload and processing of a file, extracting text and generating embeddings.
    Args:
        document (UploadFile): The uploaded document.
        db (AsyncSession): The database session.
    Returns:
        dict: Information about the uploaded file.
    """
    content = await document.read()

    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    extracted_text, valid_embeddings = await process_text_and_generate_embeddings(content)

    if not valid_embeddings:
        raise HTTPException(status_code=400, detail="No valid embeddings created.")

    file_entry = FileModel(
        filename=document.filename,
        content=content,
        extracted_text=extracted_text,
        embedding=valid_embeddings[0].tolist()
    )
        
    repo = FileRepository(db)
    await repo.add_file(file_entry)

    return {
        "filename": document.filename,
        "message": "File uploaded successfully.",
        "extracted_text": extracted_text[:100],
        "embedding_size": len(valid_embeddings)
    }
