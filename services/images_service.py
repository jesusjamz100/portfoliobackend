import os
import io
import json
import tempfile
import firebase_admin
from PIL import Image
from firebase_admin import credentials, storage

class ImageService:

    def convert_and_resize_image(self, image_bytes: bytes):
        image = Image.open(io.BytesIO(image_bytes))

        if image.mode != "RGB":
            image = image.convert('RGB')

        width, height = 730, 350
        resized_image = image.resize((width, height))

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file_path = temp_file.name
            resized_image.save(temp_file_path, "JPEG")

        return temp_file_path


    def upload_to_firebase(self, image_file: str, title: str):

        certificate_str = os.environ.get('CREDENTIALS_FB')
        certificate_dict = json.loads(certificate_str)

        cred = credentials.Certificate(certificate_dict)
        firebase_admin.initialize_app(cred)

        bucket = storage.bucket(os.environ.get('BUCKET_FB'))

        blob = bucket.blob(f'portfolioimgs/{title}.jpg')
        
        blob.upload_from_filename(image_file, content_type='image/jpeg')
        
        blob.make_public()

        os.remove(image_file)

        return blob.public_url

images_service = ImageService()

# SCOPES = ['https://www.googleapis.com/auth/drive']

# def upload_to_google_drive(image_file, title):

#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     service = build('drive', 'v3', credentials=creds)

#     file_metadata = {
#         'name': f'{title}.jpg',
#         'parents': [],
#         'visibility': 'public'
#     }

#     media = MediaFileUpload(image_file, mimetype='image/jpeg')
#     file = service.files().create(body=file_metadata,
#                                   media_body=media,
#                                   fields='id').execute()
        
#     return f"https://drive.google.com/thumbnail?id={file['id']}"