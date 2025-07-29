# rag_tool.py

from langchain.tools import Tool
from faiss_db import retrieve_docs

def rag_search(query: str) -> str:
    """Performs similarity search over ingested documents."""
    docs = retrieve_docs(query)
    if not docs:
        return "No relevant documents found."

    combined = "\n---\n".join(doc.page_content for doc in docs)
    return f"Here’s what I found:\n\n{combined}"

# Export as LangChain Tool
rag_tool = Tool(
    name="DocumentRetriever",
    func=rag_search,
    description="Useful for answering questions using ingested PDFs or nutrition documents."
)
