from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from contextlib import asynccontextmanager
from framework.database import SessionLocal, init_db
from usecases.upload_usecase import upload_file_usecase
from usecases.search_usecase import search_similar_files_usecase
from usecases.question_usecases import process_question_answer


app = FastAPI(title="BCG X Challenger API",
              description="This is the API documentation for BCG X Challenger. It allows you to interact with the application's endpoints.",
              version="1.0.1",
              contact={
                  "name": "Github",
                  "url": "https://github.com/joelmaykon94/bcgx-challenger",
              },
              license_info={
                  "name": "MIT License",
                  "url": "https://opensource.org/licenses/MIT",
              },)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()

    yield
    print("Shutting down...")

app.lifespan = lifespan


@app.post("/upload_file")
async def handle_upload_file(document: UploadFile = File(...)):
    async with SessionLocal() as db:
        try:
            return await upload_file_usecase(document, db)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
async def handle_search_similarity(query: str, top_k: int = Query(10, le=20)):
    async with SessionLocal() as db:
        try:
            return await search_similar_files_usecase(query, top_k, db)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/answer")
async def answer_question_endpoint(question: str, top_k: int = 5):
    async with SessionLocal() as db:
        try:
            return await process_question_answer(question, top_k, db)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
