import datetime
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
GOOGLE_CREDENTIALS_FILE  = './google-credentials.json'

def get_service():
    credentials_path = os.path.join(os.getcwd(), GOOGLE_CREDENTIALS_FILE)
    credentials = Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)
    return service


def create_google_calendar_event(summary, description, start_time, end_time, attendees_emails):
    service = get_service()

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',
        },
        # 'attendees': [{'email': email} for email in attendees_emails],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    try:
        # Insert the event into the Google Calendar
        event = service.events().insert(
            calendarId=settings.GOOGLE_CALENDAR_ID, body=event
        ).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return event.get('htmlLink')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None