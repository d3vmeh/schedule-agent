from dotenv import load_dotenv
from openai_tools import add_calendar_event, get_time_info
import asyncio

from agents import Agent, Runner, function_tool, SQLiteSession


load_dotenv(override=True)

prompt = f"""

    You are a helpful assistant with access to Google Calendar. You can help users schedule events and manage their calendar.

    {get_time_info()}

    When the user provides information about an event, add that event to their calendar with the exact details provided.
    If the user omits specifics about a basic property, like the date , it is permissible to use common sense to make an inference there.

    For example, if the user asks: "I'm going to see a movie at 3pm on Tuesday," you may assume the event is for the closest upcoming Tuesday.

    You have access to the following tools to complete the task the user asks you.
    - add_calendar_event()

    if you make any changes to the user's calendar, include a summary of those changes below.
    """

agent = Agent(
    name="Assistant",
    model="gpt-5-mini",
    instructions=prompt,
    tools=[function_tool(add_calendar_event)]
)

session = SQLiteSession("conversation_memory")
async def main():
    while True:
        user_query = input("[user]: ")
        result = await Runner.run(agent, input=user_query, session=session)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())