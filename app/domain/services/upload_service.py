import requests
from core.settings import settings
from domain.models.upload_model import UploadResponse

class UploadService:
    @staticmethod
    def upload_file(file):
        url = f"{settings.API_URL}/files/upload"
        try:
            files = {'file': file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            message = data.get('response', {}).get('message', "")
            filename = data.get('response', {}).get('filename', "")
            return UploadResponse(message=message, filename=filename)
        except requests.exceptions.HTTPError as http_err:
            return {"answer": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"answer": f"An error occurred: {err}"}
