# app/services/vector_db.py
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def get_vector_store():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local("taxcrm_vector_index", embeddings)
