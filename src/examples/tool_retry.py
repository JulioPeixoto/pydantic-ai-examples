from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel
from settings import settings


class ChatResult(BaseModel):
    user_id: int
    message: str


class DatabaseConn:
    def __init__(self):
        self.users = {"John Doe": 123, "Jane Smith": 456}

    def get(self, name: str) -> int | None:
        return self.users.get(name)


class AgentResponse:
    def __init__(self):
        provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
        model = OpenAIChatModel("gpt-4o-mini", provider=provider)
        self.agent = Agent(
            model=model,
            instructions="You are a helpful assistant that can answer questions and help with tasks.",
            deps_type=DatabaseConn,
            output_type=ChatResult,
        )

        self._register_tools()

    def _register_tools(self):
        @self.agent.tool(retries=2)
        def get_user_by_name(ctx: RunContext[DatabaseConn], name: str) -> int:
            print(f"Searching for user: {name}")
            # > John
            # > John Doe
            user_id = ctx.deps.get(name=name)
            if user_id is None:
                raise ModelRetry(
                    f"No user found with name {name!r}, remember to provide their full name"
                )
            return user_id

    async def invoke_agent(self, prompt: str) -> str:
        db_conn = DatabaseConn()
        response = await self.agent.run(prompt, deps=db_conn)
        return response
