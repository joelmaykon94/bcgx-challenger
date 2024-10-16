from fastapi import FastAPI, File, HTTPException, UploadFile, Depends
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import io

from domain.models import FileModel
from framework.database import SessionLocal, init_db
from usecases.upload_usecase import upload_file_usecase
from usecases.question_usecases import process_question_answer

app = FastAPI(
    title="BCG X Challenger API",
    description="This is the API documentation for BCG X Challenger. It allows you to interact with the application's endpoints.",
    version="1.0.1",
    contact={
        "name": "Github",
        "url": "https://github.com/joelmaykon94/bcgx-challenger",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()  
    yield
    print("Shutting down...")

app.lifespan = lifespan

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.post("/upload_file")
async def handle_upload_file(document: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        return await upload_file_usecase(document, db)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error uploading file.")

@app.post("/answer")
async def answer_question_endpoint(question: str, top_k: int = 5, db: AsyncSession = Depends(get_db)):
    return await process_question_answer(question, top_k, db)


@app.get("/list_pdfs")
async def list_pdfs(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(FileModel).where(FileModel.filename.like('%.pdf')))
        pdf_files = result.scalars().all()

        if not pdf_files:
            raise HTTPException(status_code=404, detail="No PDF files found.")
        
        return [{"id": file.id, "filename": file.filename} for file in pdf_files]
    except Exception as e:
        print(f"Error in list_pdfs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving PDF list.")

@app.get("/get_pdf/{filename}")
async def get_pdf(filename: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(FileModel).where(FileModel.filename == filename))
        file = result.scalar_one_or_none()

        if file and file.content:  # Check if content is not None
            return StreamingResponse(io.BytesIO(file.content), media_type='application/pdf', headers={'Content-Disposition': f'attachment; filename={filename}'})
        else:
            raise HTTPException(status_code=404, detail="PDF file not found.")
    except Exception as e:
        print(f"Error in get_pdf: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving PDF.")
