from langchain_openai import ChatOpenAI

# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini")

print("🤖 Your AI Agent is ready! (type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break
    
    response = llm.invoke(user_input)
    print("Agent:", response.content)

