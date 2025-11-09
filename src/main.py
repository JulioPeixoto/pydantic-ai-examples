from fastapi import FastAPI

from examples.hello_world import AgentResponse
from examples.tool_retry import AgentResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/agent")
async def agent_endpoint(prompt: str):
    agent_response = AgentResponse()
    return await agent_response.invoke_agent(prompt)


@app.get("/tool-retry")
async def tool_retry_endpoint(prompt: str):
    """
    Example: Send a message to John Doe asking for coffee next week
    """
    tool_retry = AgentResponse()
    return await tool_retry.invoke_agent(prompt)
