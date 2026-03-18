from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

# 1. Load text
loader = TextLoader("mod3_retrieval/knowledge.txt")
documents = loader.load()

# 2. Manual chunking
texts = []
for doc in documents:
    content = doc.page_content
    for i in range(0, len(content), 300):
        texts.append(content[i:i+300])

# 3. Local embeddings (FREE)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Vector store
vectorstore = FAISS.from_texts(texts, embeddings)

# 5. Retrieve relevant context
query = "What is the difference between machine learning and deep learning?"
docs = vectorstore.similarity_search(query, k=2)

context = "\n".join([d.page_content for d in docs])

# 6. Local LLM (OLLAMA)
llm = Ollama(model="tinyllama")

prompt = f"""
Answer the question ONLY using the context below.

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

print("Answer:\n", response)

