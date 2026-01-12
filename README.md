# Schedule Agent

An AI-powered scheduling assistant that integrates with Google Calendar. The project includes two implementations:
- **OpenAI SDK Agent**: Using OpenAI's Agents SDK
- **Google ADK Agent**: Using Google's Agentic Development Kit (ADK)

The agents can understand natural language requests and manage your calendar with full CRUD operations and proper timezone handling.

## Features

- **Full Calendar Management**
  - Create, read, and delete calendar events
  - View upcoming events and schedules
  - Support for multiple calendars (personal, work, etc.)
  - List and switch between different calendars

- **Natural Language Processing**
  - Automatic timezone detection and handling
  - Support for relative time references (e.g., "tomorrow", "next week", "in 2 hours")
  - Interpret vague requests with intelligent defaults

- **Event Customization**
  - Event details including title, description, location, and custom time ranges
  - Flexible time formats (ISO format or natural language)

- **Security & Authentication**
  - Google Calendar integration via OAuth 2.0
  - Secure credential management with token persistence
  - Separate credentials for each agent implementation

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (for OpenAI SDK agent)
- Google Gemini API Key (for Google ADK agent)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/d3vmeh/schedule-agent
cd schedule-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Calendar API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the appropriate folder:
     - `openai_sdk_agent/credentials.json` for OpenAI SDK agent
     - `google_adk_agent/credentials.json` for Google ADK agent

4. Set up environment variables:

   **For OpenAI SDK Agent:**
   - Create a `.env` file in `openai_sdk_agent/`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

   **For Google ADK Agent:**
   - Create a `.env` file in `google_adk_agent/`
   - Add your API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

### OpenAI SDK Agent

Run the OpenAI SDK agent:
```bash
cd openai_sdk_agent
python openai_agent.py
```

### Google ADK Agent

Run the Google ADK agent (must be in the parent directory):
```bash
adk web
```

Or use the CLI interface:
```bash
adk run google_adk_agent
```

### Example Requests

The agents support a wide range of natural language requests:

**Creating Events:**
- "Schedule a team meeting tomorrow at 2pm"
- "Add a doctor's appointment next Monday at 10am for 30 minutes"
- "Create an event called 'Lunch with Sarah' at noon on Friday at Main Street Cafe"

**Viewing Events:**
- "What's on my calendar today?"
- "Show me my upcoming events"
- "What do I have this week?"
- "Any events tomorrow?"

**Managing Multiple Calendars:**
- "Show me all my calendars"
- "Add a meeting to my work calendar tomorrow at 3pm"
- "What's on my personal calendar this weekend?"

**Deleting Events:**
- "Delete my 2pm meeting today"
- "Remove the dentist appointment on Friday"
- "Cancel all events on Tuesday"

On first run, the application will open a browser window for Google OAuth authorization. After authorization, credentials are saved to `google_adk_agent/token.json` or `openai_sdk_agent/token.json` for future use.

## How It Works

1. The agent receives natural language input from the user
2. Using the current date/time and timezone information, it interprets relative time references
3. The agent determines which calendar operation is needed:
   - `list_calendars()` - Lists all available calendars
   - `get_calendar_events()` - Retrieves events from a specific calendar
   - `add_calendar_event()` - Creates a new event with properly formatted datetime strings
   - `delete_calendar_event()` - Removes an event by its ID
4. The function authenticates with Google Calendar (using saved credentials or OAuth flow)
5. The operation is performed and a confirmation is returned

## Available Tools

Both agents have access to the following calendar management tools:

- **`list_calendars()`** - List all calendars accessible to the user
- **`get_calendar_events(calendar_id, time_min, time_max, max_results)`** - Retrieve events from a calendar
- **`add_calendar_event(summary, start_time, calendar_id, end_time, description, location)`** - Add a new event
- **`delete_calendar_event(event_id, calendar_id)`** - Delete an existing event

## Project Structure

```
schedule-agent/
├── google_adk_agent/
│   ├── agent.py           # Google ADK agent configuration
│   ├── adk_tools.py       # Calendar API tools
│   ├── __init__.py
│   └── credentials.json   # Google OAuth credentials (you provide)
├── openai_sdk_agent/
│   ├── openai_agent.py    # OpenAI SDK agent configuration
│   ├── openai_tools.py    # Calendar API tools
│   ├── credentials.json   # Google OAuth credentials (you provide)
│   └── .env              # OpenAI API key (you provide)
├── requirements.txt
└── README.md
```

## Future Enhancements

- Update/modify existing calendar events
- Sharing calendar invites via email
- Recurring events support
- Event reminders and notifications
- Calendar event search and filtering
