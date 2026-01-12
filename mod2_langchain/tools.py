from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType


# Tool: simple calculator
import re

def multiply_numbers(input_text: str) -> str:
    # Extract numbers safely using regex
    numbers = re.findall(r"\d+", input_text)

    if len(numbers) < 2:
        return "Error: Please provide two numbers."

    a, b = map(int, numbers[:2])
    return str(a * b)


tools = [
    Tool(
        name="Multiply",
        func=multiply_numbers,
        description="Use this tool to multiply two integers."
    )
]

llm = ChatOpenAI(model="gpt-4o-mini")

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

print(agent.run("Multiply 12 and 9 for me."))
