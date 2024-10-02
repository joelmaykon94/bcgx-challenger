from fastapi import FastAPI, File, Query, UploadFile
from contextlib import asynccontextmanager
from framework.database import init_db
from usecases.file_usecases import upload_file, search_similar_files

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
    # Code to run at startup
    print("Starting up...")
    await init_db()

    yield
    # Code to run at shutdown
    print("Shutting down...")

app.lifespan = lifespan


@app.post("/upload_file")
async def handle_upload_file(document: UploadFile = File(...)):
    return await upload_file(document)


@app.get("/search")
async def handle_search_similarity(query: str, top_k: int = Query(10, le=20)):
    return await search_similar_files(query, top_k)
