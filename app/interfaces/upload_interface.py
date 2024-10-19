from domain.services.upload_service import UploadService

def handle_upload(file):
    if file:
       return UploadService.upload_file(file)