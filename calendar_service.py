from googleapiclient.discovery import build
from google_auth import get_credentials

def build_calendar_service():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    return service
