import logging
import os

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routers import files_router
from services.files_service import FilesService
from utils.store import get_store

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(files_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"message": "OK"}

@app.on_event("startup")
async def startup_event():
    vectorstore = get_store()
    BRONZE_DIRECTORY = '/app/medalion/bronze'

    if not os.path.exists(BRONZE_DIRECTORY):
        print(f"Directory {BRONZE_DIRECTORY} does not exist.")
        return
    
    for filename in os.listdir(BRONZE_DIRECTORY):
        if filename.endswith(".pdf"):
            file_path = os.path.join(BRONZE_DIRECTORY, filename)
            print(f"Uploading file: {file_path}")
            chunk_size = 200
            async with open(file_path, "rb") as file: 
                response = await FilesService.upload(file, chunk_size, vectorstore)
                print(response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["FASTAPI_PORT"]))