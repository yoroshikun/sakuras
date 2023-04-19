import chromadb
import os
from chromadb.utils import embedding_functions
from chromadb.config import Settings

chroma_client = chromadb.Client(Settings(
    chroma_api_impl="rest",
    chroma_server_host=os.environ.get("CHROMA_HOST", "0.0.0.0"),
    chroma_server_http_port="8000"
    ))

def init_collection(name: str):
    chroma_client.create_collection(name="test")

def generate_embedding(text: str):
    # instructor models in the future
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

