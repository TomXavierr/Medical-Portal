# from django.conf import settings
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request
# import os

# # If modifying these SCOPES, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# def create_google_calendar_event(summary, description, start_time, end_time, attendees_emails):
#     creds = None
#     client_secret_file = settings.GOOGLE_CLIENT_SECRET_FILE
#     token_path = settings.GOOGLE_TOKEN_FILE

#     if os.path.exists(token_path):
#         creds = Credentials.from_authorized_user_file(token_path, settings.GOOGLE_SCOPES)
    
#     # If no (valid) credentials available, prompt the user to log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, settings.GOOGLE_SCOPES)
#             creds = flow.run_local_server(port=0)

#         with open(token_path, 'w') as token:
#             token.write(creds.to_json())

#     try:
#         service = build('calendar', 'v3', credentials=creds)

#         event = {
#             'summary': summary,
#             'description': description,
#             'start': {
#                 'dateTime': start_time,
#                 'timeZone': 'Asia/Kolkata',  
#             },
#             'end': {
#                 'dateTime': end_time,
#                 'timeZone': 'Asia/Kolkata', 
#             },
#             'attendees': [{'email': email} for email in attendees_emails],
#             'reminders': {
#                 'useDefault': False,
#                 'overrides': [
#                     {'method': 'email', 'minutes': 24 * 60},
#                     {'method': 'popup', 'minutes': 10},
#                 ],
#             },
#         }

#         event = service.events().insert(calendarId='primary', body=event).execute()
#         print('Event created: %s' % (event.get('htmlLink')))
#         return event.get('htmlLink')

#     except Exception as e:
#         print(f'An error occurred: {e}')
#         return None