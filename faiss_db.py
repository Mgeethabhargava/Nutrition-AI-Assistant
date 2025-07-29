# faiss_db.py

import os
from langchain.vectorstores import FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv
load_dotenv()

VECTOR_DB_FOLDER = "vectorstore"
CHROMA_DB_FOLDER = "chroma_fallback"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embedding = OpenAIEmbeddings()

def load_vectorstore() -> FAISS:
    """Load FAISS vectorstore if available, else return empty FAISS."""
    if os.path.exists(os.path.join(VECTOR_DB_FOLDER, "index.faiss")):
        return FAISS.load_local(VECTOR_DB_FOLDER, embedding, allow_dangerous_deserialization=True)
    return FAISS.from_documents([], embedding)

def fallback_chroma_store() -> Chroma:
    """Optional fallback retriever using Chroma if FAISS not found or empty."""
    os.makedirs(CHROMA_DB_FOLDER, exist_ok=True)
    return Chroma(persist_directory=CHROMA_DB_FOLDER, embedding_function=embedding)

def retrieve_docs(query: str, k: int = 3) -> list[Document]:
    """Try retrieving from FAISS; fallback to Chroma if needed."""
    try:
        db = load_vectorstore()
        results = db.similarity_search(query, k=k)
        if not results:
            raise ValueError("No results from FAISS.")
        return results
    except Exception as e:
        print(f"[FAISS Error]: {e} — Falling back to Chroma.")
        chroma = fallback_chroma_store()
        return chroma.similarity_search(query, k=k)
