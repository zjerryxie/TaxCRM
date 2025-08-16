# app/services/vector_db.py
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def get_vector_store():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local("taxcrm_vector_index", embeddings)

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

def init_vector_store(clients: list[dict]):
    """Initialize FAISS with client data."""
    texts = [f"{c['filing_status']} {c['tax_year']}" for c in clients]  # Customize embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
    return FAISS.from_texts(texts, embeddings)

def save_vector_store(store, path: str = "taxcrm_faiss_index"):
    store.save_local(path)
