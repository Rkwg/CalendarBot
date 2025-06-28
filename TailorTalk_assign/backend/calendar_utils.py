from datetime import datetime, timedelta
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
from urllib.parse import quote
import json
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_INFO = json.loads(os.environ["SERVICE_ACCOUNT_INFO"])

credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)
CALENDAR_ID = "1aded8a9867b975352ac1ae4460eef71699c173034659d3faf34b2c577698966@group.calendar.google.com"

def get_availability(start_time, end_time):
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])


def book_event(summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

    # Format for public embed calendar URL
    calendar_id = CALENDAR_ID  
    start_utc = start_time.astimezone(pytz.UTC).strftime('%Y%m%dT%H%M%SZ')
    end_utc = end_time.astimezone(pytz.UTC).strftime('%Y%m%dT%H%M%SZ')
    
    embed_url = (
        f"https://calendar.google.com/calendar/embed?"
        f"src={quote(calendar_id)}"
        f"&dates={start_utc}/{end_utc}"
    )

    return embed_url
