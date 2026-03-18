import streamlit as st
import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama


st.set_page_config(page_title="PDF Agent", layout="wide")

st.title("📘 Local PDF Study Agent")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pdf_agent", "faiss_index")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

llm = Ollama(model="tinyllama")   


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


prompt = st.chat_input("Ask your PDF...")


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    docs = vectorstore.similarity_search(prompt, k=3)
    context = "\n".join([d.page_content for d in docs])

    full_prompt = f"""
    Answer ONLY from the context below.

    Context:
    {context}

    Question:
    {prompt}
    """

    response = llm.invoke(full_prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)
