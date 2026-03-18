import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "sample.pdf")
DB_PATH = os.path.join(BASE_DIR, "faiss_index")

print("Loading PDF...")

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print(f"Loaded {len(documents)} pages.")

texts = []
for doc in documents:
    content = doc.page_content
    for i in range(0, len(content), 500):
        texts.append(content[i:i+500])

print(f"Created {len(texts)} chunks.")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating vector database...")

os.makedirs(DB_PATH, exist_ok=True)

vectorstore = FAISS.from_texts(texts, embeddings)
vectorstore.save_local(DB_PATH)

print("✅ Vector DB built successfully!")
print("Location:", DB_PATH)

