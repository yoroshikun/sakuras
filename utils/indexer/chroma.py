import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()

def init_collection(name: str):
    chroma_client.create_collection(name="test")

def generate_embedding(text: str):
    # instructor models in the future
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

