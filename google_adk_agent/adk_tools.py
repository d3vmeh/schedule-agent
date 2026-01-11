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

# Get the directory where this module is located, making sure it is properly finding credentials.json
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_CREDENTIALS_PATH = os.path.join(_MODULE_DIR, 'credentials.json')
_TOKEN_PATH = os.path.join(_MODULE_DIR, 'token.json')

def get_calendar_service():
    """
    Authenticate and return Google Calendar service object.

    This function handles OAuth 2.0 authentication. On first run, it will open
    a browser window for user authorization. Credentials are saved to token.json
    for future use.
    """
    creds = None

    if os.path.exists(_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(_CREDENTIALS_PATH):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console.\n"
                    "See: https://developers.google.com/calendar/api/quickstart/python"
                )
            flow = InstalledAppFlow.from_client_secrets_file(_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

# Agent tools
def list_calendars() -> dict:
    """
    List all calendars accessible to the user.

    Returns:
        dict: Dictionary containing:
            - success: Boolean indicating if the request was successful
            - calendars: List of calendars with their details (id, summary, description, primary)
            - count: Number of calendars returned

    Example:
        list_calendars()
    """
    try:
        service = get_calendar_service()

        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        formatted_calendars = []
        for calendar in calendars:
            formatted_calendar = {
                'id': calendar['id'],
                'summary': calendar.get('summary', 'No name'),
                'primary': calendar.get('primary', False),
            }

            if 'description' in calendar:
                formatted_calendar['description'] = calendar['description']
            if 'backgroundColor' in calendar:
                formatted_calendar['color'] = calendar['backgroundColor']

            formatted_calendars.append(formatted_calendar)

        return {
            'success': True,
            'calendars': formatted_calendars,
            'count': len(formatted_calendars)
        }

    except HttpError as error:
        return {
            'success': False,
            'error': f'An error occurred: {error}',
            'calendars': [],
            'count': 0
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'An error occurred: {str(e)}',
            'calendars': [],
            'count': 0
        }


def get_calendar_events(
    calendar_id: str = 'primary',
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    max_results: int = 10,
    timezone: Optional[str] = None
) -> dict:
    """
    Retrieve events from Google Calendar.

    Args:
        calendar_id: Calendar ID to query (default: 'primary'). Use list_calendars() to get available calendar IDs.
        time_min: Start of time range in ISO format (e.g., '2025-01-15T00:00:00').
                  If not provided, defaults to current time.
        time_max: End of time range in ISO format (e.g., '2025-01-22T23:59:59').
                  If not provided, retrieves events indefinitely into the future.
        max_results: Maximum number of events to return (default: 10, max: 2500)
        timezone: Timezone for the query (default: system timezone)

    Returns:
        dict: Dictionary containing:
            - success: Boolean indicating if the request was successful
            - events: List of events with their details
            - count: Number of events returned
            - calendar_id: The calendar that was queried

    Example:
        # Get next 10 upcoming events from primary calendar
        get_calendar_events()

        # Get events for a specific day from a specific calendar
        get_calendar_events(
            calendar_id="user@example.com",
            time_min="2025-01-15T00:00:00",
            time_max="2025-01-15T23:59:59"
        )
    """
    try:
        service = get_calendar_service()

        if timezone is None:
            timezone = get_system_timezone()

        # Default to current time if not specified
        if time_min is None:
            time_min = datetime.now().isoformat()

        # Ensure datetime strings are in RFC3339 format with timezone
        # If they don't already have timezone info, add 'Z' for UTC or parse with timezone
        if time_min and not time_min.endswith('Z') and '+' not in time_min and time_min.count('-') == 2:
            # Parse the datetime and add timezone
            dt = datetime.fromisoformat(time_min.replace('Z', '+00:00'))
            time_min = dt.isoformat() + 'Z' if dt.tzinfo is None else dt.isoformat()

        if time_max and not time_max.endswith('Z') and '+' not in time_max and time_max.count('-') == 2:
            # Parse the datetime and add timezone
            dt = datetime.fromisoformat(time_max.replace('Z', '+00:00'))
            time_max = dt.isoformat() + 'Z' if dt.tzinfo is None else dt.isoformat()

        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        # Formatting event results
        formatted_events = []
        for event in events:
            formatted_event = {
                'id': event['id'],
                'summary': event.get('summary', 'No title'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date')),
            }

            if 'description' in event:
                formatted_event['description'] = event['description']
            if 'location' in event:
                formatted_event['location'] = event['location']
            if 'htmlLink' in event:
                formatted_event['link'] = event['htmlLink']

            formatted_events.append(formatted_event)

        return {
            'success': True,
            'events': formatted_events,
            'count': len(formatted_events),
            'calendar_id': calendar_id
        }

    except HttpError as error:
        return {
            'success': False,
            'error': f'An error occurred: {error}',
            'events': [],
            'count': 0
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'An error occurred: {str(e)}',
            'events': [],
            'count': 0
        }


def delete_calendar_event(
    event_id: str,
    calendar_id: str = 'primary'
) -> dict:
    """
    Delete an event from Google Calendar.

    Args:
        event_id: The ID of the event to delete (required). Can be obtained from get_calendar_events().
        calendar_id: Calendar ID where the event exists (default: 'primary')

    Returns:
        dict: Dictionary containing:
            - success: Boolean indicating if the deletion was successful
            - event_id: The ID of the deleted event
            - calendar_id: The calendar from which the event was deleted
            - message: Success or error message

    Example:
        delete_calendar_event(event_id="abc123def456")
    """
    try:
        service = get_calendar_service()

        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

        return {
            'success': True,
            'event_id': event_id,
            'calendar_id': calendar_id,
            'message': f'Event successfully deleted from calendar'
        }

    except HttpError as error:
        return {
            'success': False,
            'event_id': event_id,
            'calendar_id': calendar_id,
            'error': f'An error occurred: {error}'
        }
    except Exception as e:
        return {
            'success': False,
            'event_id': event_id,
            'calendar_id': calendar_id,
            'error': f'An error occurred: {str(e)}'
        }


def add_calendar_event(
    summary: str,
    start_time: str,
    calendar_id: str = 'primary',
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
        calendar_id: Calendar ID to add event to (default: 'primary'). Use list_calendars() to get available calendar IDs.
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

        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

        return {
            'success': True,
            'event_id': created_event['id'],
            'event_link': created_event.get('htmlLink'),
            'summary': created_event['summary'],
            'start': created_event['start'].get('dateTime'),
            'end': created_event['end'].get('dateTime'),
            'calendar_id': calendar_id
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


# Helper functions for prompt
def get_system_timezone():
    return str(get_localzone())

def get_time_info():
    now = datetime.now()
    local_timezone = get_localzone()
    timezone_name = str(local_timezone)

    current_date = now.strftime('%Y-%m-%d')
    current_day = now.strftime('%A')
    current_time = now.strftime('%I:%M %p')
    current_datetime = now.strftime('%Y-%m-%d %I:%M %p')

    datetime_info = f"""Here is the current datetime information:
    - Date: {current_date}
    - Day of week: {current_day}
    - Time: {current_time}
    - Full datetime: {current_datetime}
    - Timezone: {timezone_name}

    When users mention relative times like "tomorrow", "next week", or "in 2 hours", calculate the exact datetime based on the current information above.
    Always use ISO format (YYYY-MM-DDTHH:MM:SS) when calling the add_calendar_event function.
    Use the timezone "{timezone_name}" for all calendar events.

    """
    return datetime_info
