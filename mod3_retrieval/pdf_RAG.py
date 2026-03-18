import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

# -------- PATH SAFETY (important) --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE_DIR, "sample.pdf")

# -------- LOAD PDF --------
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"Loaded {len(documents)} pages.")

# -------- SIMPLE CHUNKING --------
texts = []
for doc in documents:
    content = doc.page_content
    for i in range(0, len(content), 500):
        texts.append(content[i:i+500])

print(f"Created {len(texts)} chunks.")

# -------- LOCAL EMBEDDINGS --------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------- VECTOR DB --------
vectorstore = FAISS.from_texts(texts, embeddings)

print("Vector store ready.")

# -------- LOCAL LLM --------
llm = Ollama(model="tinyllama")  

# -------- ASK LOOP --------
while True:
    query = input("\nAsk your PDF (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    docs = vectorstore.similarity_search(query, k=3)
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    Answer ONLY from the context below.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    print("\nAnswer:\n", response)
