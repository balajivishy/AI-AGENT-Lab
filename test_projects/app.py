import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load API key
load_dotenv()

# Setup model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Setup memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.memory,
    verbose=True
)

# Streamlit UI
st.title("🤖 AI Agent Chat")
st.write("Chat with your first AI Agent — with memory!")

user_input = st.text_input("You:", "")

if user_input:
    response = conversation.predict(input=user_input)
    st.write(f"**Agent:** {response}")