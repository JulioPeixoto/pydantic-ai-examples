from fastapi import FastAPI

from examples.hello_world import AgentResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/agent")
async def agent_endpoint(prompt: str):
    agent_response = AgentResponse()
    return await agent_response.invoke_agent(prompt)