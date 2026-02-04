import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# Config from env or json file
# For this MVP, we assume headers are set in env or client_secret.json is provided
# We will use env vars for simplicity if possible, or expect client_secrets.json

CLIENT_CONFIG = {
    "web": {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_auth_url(redirect_uri):
    """Generates the OAuth2 URL."""
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return auth_url

def exchange_code(code, redirect_uri):
    """Exchanges code for tokens."""
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    return {
        "refresh_token": creds.refresh_token,
        "access_token": creds.token,
        "scopes": creds.scopes
    }

def get_drive_service(access_token, refresh_token=None):
    """Returns a build service object."""
    creds = Credentials(
        access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def upload_file(service, file_data, filename, folder_id=None, mime_type='image/jpeg'):
    """Uploads a file to Drive."""
    file_metadata = {'name': filename}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaIoBaseUpload(io.BytesIO(file_data), mimetype=mime_type, resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webContentLink, webViewLink'
    ).execute()
    
    return file

def create_folder(service, folder_name, parent_id=None):
    """Creates a folder and returns its ID."""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
        
    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

def set_file_public(service, file_id):
    """Sets the file permission to anyone with link (reader)."""
    user_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ).execute()
