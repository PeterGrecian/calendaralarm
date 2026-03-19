#!/usr/bin/env python3
"""List upcoming calendar events."""

import datetime
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = os.path.expanduser('~/.config/gcloud/calendar-client.json')
TOKEN_FILE = os.path.expanduser('~/.config/gcloud/calendar-token.json')

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return creds

service = build('calendar', 'v3', credentials=get_credentials())

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = service.events().list(
    calendarId='primary',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = result.get('items', [])
if not events:
    print('No upcoming events.')
else:
    for e in events:
        start = e['start'].get('dateTime', e['start'].get('date'))
        print(f"{start}  {e.get('summary', '(no title)')}")
