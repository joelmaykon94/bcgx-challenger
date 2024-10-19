import requests
from core.settings import settings
from domain.models.query_model import QueryResponse

class QueryService:
    @staticmethod
    def get_qna(question):
        url = f"{settings.API_URL}/files/query"
        params = {
            "question": question,
            "temperature": 0.6,
            "n_docs": 3
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            answer = data.get('answer', "Erro ao buscar resposta.")
            return QueryResponse(answer=answer)
        except requests.exceptions.HTTPError as http_err:
            return {"answer": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"answer": f"An error occurred: {err}"}
