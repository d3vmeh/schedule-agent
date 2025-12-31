import os
import json
from datetime import datetime, timedelta
from typing import Optional
from tzlocal import get_localzone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_system_timezone():
    return str(get_localzone())

def get_calendar_service():
    """
    Authenticate and return Google Calendar service object.

    This function handles OAuth 2.0 authentication. On first run, it will open
    a browser window for user authorization. Credentials are saved to token.json
    for future use.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console.\n"
                    "See: https://developers.google.com/calendar/api/quickstart/python"
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def add_calendar_event(
    summary: str,
    start_time: str,
    end_time: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    timezone: Optional[str] = None
) -> dict:
    """
    Add an event to Google Calendar.

    Args:
        summary: Event title/summary (required)
        start_time: Start time in ISO format (e.g., '2024-01-15T10:00:00') or natural language
        end_time: End time in ISO format. If not provided, defaults to 1 hour after start_time
        description: Event description (optional)
        location: Event location (optional)
        timezone: Timezone for the event (default: system timezone)

    Returns:
        dict: Created event details including event ID and link

    Example:
        add_calendar_event(
            summary="Team Meeting",
            start_time="2025-01-15T10:00:00",
            end_time="2025-01-15T11:00:00",
            description="Discuss Q1 goals",
            location="Conference Room A"
        )
    """
    try:
        service = get_calendar_service()

        if timezone is None:
            timezone = get_system_timezone()

        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))

        if end_time is None:
            end_dt = start_dt + timedelta(hours=1)
        else:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': timezone,
            },
        }

        if description:
            event['description'] = description

        if location:
            event['location'] = location

        created_event = service.events().insert(calendarId='primary', body=event).execute()

        return {
            'success': True,
            'event_id': created_event['id'],
            'event_link': created_event.get('htmlLink'),
            'summary': created_event['summary'],
            'start': created_event['start'].get('dateTime'),
            'end': created_event['end'].get('dateTime'),
        }

    except HttpError as error:
        return {
            'success': False,
            'error': f'An error occurred: {error}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }
