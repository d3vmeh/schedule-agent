from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from .adk_tools import add_calendar_event, get_calendar_events, delete_calendar_event, update_calendar_event, list_calendars, invite_to_event, get_time_info



sharing_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful schedule management assistant to help the user manage their calendar and tasks.',
    instruction=f"""
    You are a helpful assistant with access to Google Calendar. You can help users invite people to Google Calendar events

    {get_time_info()}


    You have access to the following tools to complete the task the user asks you.
    - invite_to_event() - Add attendees to an existing event and send email invitations

    """,
    tools = [invite_to_event]
)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful schedule management assistant to help the user manage their calendar and tasks.',
    instruction=f"""
    You are a helpful assistant with access to Google Calendar. You can help users schedule events and manage their calendar.

    {get_time_info()}

    When the user provides information about an event, add that event to their calendar with the exact details provided.
    If the user omits specifics about a basic property, like the date , it is permissible to use common sense to make an inference there.

    For example, if the user asks: "I'm going to see a movie at 3pm on Tuesday," you may assume the event is for the closest upcoming Tuesday.

    You have access to the following tools to complete the task the user asks you.
    - list_calendars() - List all available calendars the user has access to
    - add_calendar_event() - Add a new event to a calendar (supports attendees for sending invites)
    - get_calendar_events() - Retrieve upcoming events from a calendar (supports calendar_id parameter)
    - update_calendar_event() - Update an event on a calendar (requires event_id and calendar_id)
    - delete_calendar_event() - Delete an event from a calendar (requires event_id and calendar_id)
    - invite_to_event() - Add attendees to an existing event and send email invitations

    IMPORTANT: The user may have multiple calendars. When the user mentions a specific calendar by name
    (e.g., "work calendar", "personal calendar", "family calendar"), first use list_calendars() to find
    the correct calendar_id, then use that ID with the calendar functions.

    When deleting or updating events, first use get_calendar_events() to find the event and get its event_id,
    then use delete_calendar_event() or update_calendar_event() with that ID.

    If no specific calendar is mentioned, use the primary calendar (calendar_id='primary').

    If you make any changes to the user's calendar, include a summary of those changes below.
    When the user asks about their schedule or upcoming events, use get_calendar_events() to retrieve them.

    """,
    tools = [list_calendars, add_calendar_event, get_calendar_events, update_calendar_event, delete_calendar_event, AgentTool(sharing_agent)]
)
