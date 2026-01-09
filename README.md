# Schedule Agent

An AI-powered scheduling assistant that integrates with Google Calendar. The project includes two implementations:
- **OpenAI SDK Agent**: Using OpenAI's Agents SDK
- **Google ADK Agent**: Using Google's Agentic Development Kit (ADK)

The agents can understand natural language requests and automatically create calendar events with proper timezone handling.

## Features

- Natural language processing for scheduling requests
- Google Calendar integration via OAuth 2.0
- Automatic timezone detection and handling
- Support for relative time references (e.g., "tomorrow", "next week", "in 2 hours")
- Event details including title, description, location, and custom time ranges
- Secure credential management with token persistence

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
     GOOGLE_GENAI_USE_VERTEXAI=0
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
adk run google_adk_agent
```

The agent will prompt you for input. You can make requests like:
- "Schedule a team meeting tomorrow at 2pm"
- "Add a doctor's appointment next Monday at 10am for 30 minutes"
- "Create an event called 'Lunch with Sarah' at noon on Friday at Main Street Cafe"

On first run, the application will open a browser window for Google OAuth authorization. After authorization, credentials are saved to `token.json` for future use.

## How It Works

1. The agent receives natural language input from the user
2. Using the current date/time and timezone information, it interprets relative time references
3. It calls the `add_calendar_event` function with properly formatted datetime strings
4. The function authenticates with Google Calendar (using saved credentials or OAuth flow)
5. The event is created and a confirmation is returned

## Next Steps


- Implement multi-agent framework in ADK agent (EditorAgent, ReaderAgent)
- Setup tool for sharing calendar invites via email