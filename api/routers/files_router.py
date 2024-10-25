import requests
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse


from services.files_service import FilesService
from utils.store import get_store

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/query")
async def query(
    question: str,
    temperature: float = 0.7,
    n_docs: int = 10,
    vectorstore=Depends(get_store),
):
    # result = f"<b>Pergunta:</b>{question} <br> <b>Temperatura do LLM:</b>{temperature} <br> <b>Quantidade de documentos similares:</b>{n_docs} <br> Dicas: separe a resposta um titulo em <b> <br> 🪴 Informações encontradas:</b> <br> e o resumo do comportamento ideal para a solução em um título em <br> <b>💡 Solução efetiva sugerida:</b>"
    try:
        result = await FilesService.query(question, temperature, n_docs, vectorstore)
        return JSONResponse(content={"answer": result})
    except requests.exceptions.HTTPError as http_err:
        return JSONResponse(content={"answer": f"HTTP error occurred: {http_err}"})
    except Exception as err:
        return JSONResponse(content={"answer": f"An error occurred: {err}"})


@router.post("/upload")
async def upload(
    file: UploadFile, chunk_size: int = 200, vectorstore=Depends(get_store)
):
    try:
        response = await FilesService.upload(file, chunk_size, vectorstore)
        return {"response": response}
    except requests.exceptions.HTTPError as http_err:
        return JSONResponse(content={"response": f"HTTP error occurred: {http_err}"})
    except Exception as err:
        return JSONResponse(content={"response": f"An error occurred: {err}"})
