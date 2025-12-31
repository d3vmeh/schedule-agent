from dotenv import load_dotenv
from agents import Agent, Runner
from tools import add_calendar_event

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant with access to Google Calendar. You can help users schedule events and manage their calendar.",
    tools=[add_calendar_event]
)


result = Runner.run_sync(agent, "Add an event: Work on Timeline from 10pm to 11pm on December 30th 2025.")
print(result.final_output)