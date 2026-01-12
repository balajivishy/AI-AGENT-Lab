from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda, RunnableSequence

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

step1 = RunnableLambda(lambda topic: f"Topic: {topic}")

step2 = RunnableLambda(
    lambda text: llm.invoke(f"Summarize this: {text}").content
)

chain = RunnableSequence(step1, step2)

result = chain.invoke("Quantum computing")
print(result)



