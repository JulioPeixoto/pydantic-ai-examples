from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from settings import settings


class AgentResponse:
    def __init__(self):
        provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
        model = OpenAIChatModel("gpt-4o-mini", provider=provider)
        self.agent = Agent(
            model=model,
            instructions="You are a helpful assistant that can answer questions and help with tasks.",
        )

    async def invoke_agent(self, prompt: str) -> str:
        response = await self.agent.run(prompt)
        return response
