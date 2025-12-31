from dotenv import load_dotenv
from datetime import datetime
from tzlocal import get_localzone
from agents import Agent, Runner, function_tool
from tools import add_calendar_event

import asyncio

load_dotenv(override=True)


now = datetime.now()
local_timezone = get_localzone()
timezone_name = str(local_timezone)

current_date = now.strftime('%Y-%m-%d')
current_day = now.strftime('%A')
current_time = now.strftime('%I:%M %p')
current_datetime = now.strftime('%Y-%m-%d %I:%M %p')

agent = Agent(
    name="Assistant",
    model="gpt-5-mini",
    instructions=f"""

    You are a helpful assistant with access to Google Calendar. You can help users schedule events and manage their calendar.


    Here is the current datetime information:
    - Date: {current_date}
    - Day of week: {current_day}
    - Time: {current_time}
    - Full datetime: {current_datetime}
    - Timezone: {timezone_name}

    When users mention relative times like "tomorrow", "next week", or "in 2 hours", calculate the exact datetime based on the current information above.
    Always use ISO format (YYYY-MM-DDTHH:MM:SS) when calling the add_calendar_event function.
    Use the timezone "{timezone_name}" for all calendar events.

    """,
    tools=[function_tool(add_calendar_event)]
)


async def main():
    user_query = input("[user]: ")
    result = await Runner.run(agent, input=user_query)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())