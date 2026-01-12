from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

response = llm.invoke("Explain what an AI agent is in one sentence.")
print(response)
