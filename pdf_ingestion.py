# pdf_ingestion.py

import os
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

# Set your FAISS index path
FAISS_INDEX_PATH = "faiss_index"

def ingest_pdf(file_path: str):
    """Ingests a PDF and updates the FAISS vector index."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    # Load PDF content
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Initialize embeddings
    embeddings = OpenAIEmbeddings()

    # Load or create FAISS index
    if os.path.exists(FAISS_INDEX_PATH):
        db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        db = FAISS.from_documents(documents, embeddings)

    # Add new documents to index
    db.add_documents(documents)
    db.save_local(FAISS_INDEX_PATH)

    return f"PDF '{os.path.basename(file_path)}' successfully ingested and indexed."
