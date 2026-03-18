import os

from langchain_community.llms import Ollama
from langchain.agents import create_react_agent, AgentExecutor, Tool
from langchain import hub

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# Pull standard ReAct prompt
prompt = hub.pull("hwchase17/react")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "faiss_index")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


def search_pdf(query):
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])


tools = [
    Tool(
        name="PDF Search",
        func=search_pdf,
        description="Use this tool to answer ANY question about the company, Aurex, "
        "or anything that might be contained inside the PDF. "
        "If the question relates to the document, you MUST use this tool."
    )
]


llm = Ollama(model="phi3:mini")


# ✅ CREATE AGENT
agent = create_react_agent(
    llm,
    tools,
    prompt
)

# ✅ CREATE EXECUTOR
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)



while True:

    question = input("\nAsk your agent: ")

    if question.lower() == "exit":
        break

    response = agent_executor.invoke({"input": question})

    print("\nFinal Answer:\n", response["output"])
