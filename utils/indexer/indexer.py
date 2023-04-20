from langchain.vectorstores import Chroma
from typing import Optional, Dict, List
import chromadb
import os
from langchain.embeddings.base import Embeddings
from dataclasses import dataclass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from langchain.docstore.document import Document

_LANGCHAIN_DEFAULT_COLLECTION_NAME = "langchain"
persist_dir = "db"

@dataclass
class ChromaDBSettings:
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        embedding_function: Optional[Embeddings] = None,
        persist_directory: Optional[str] = None,
        client_settings: Optional[chromadb.config.Settings] = None,
        collection_metadata: Optional[Dict] = None,
        client: Optional[chromadb.Client] = None,

@dataclass
class DocumentMetadata:
    id: str
    title: str
    createdBy: str
    createdAt: str
    space: str

@dataclass
class CollectionMetadata:
     type: str

class Indexer:
    collection_name = _LANGCHAIN_DEFAULT_COLLECTION_NAME
    metadata: Document
    db = Chroma


    def __init__(self, collection_name: str, metadata: CollectionMetadata, chroma_db_settings: ChromaDBSettings):
        self.collection_name = collection_name or chroma_db_settings.collection_name
        self.metadata = metadata             
        if chroma_db_settings is None:
             chroma_db_settings = ChromaDBSettings(collection_name)
        self.db = Chroma(
        client_settings=Settings(
            chroma_api_impl="rest",
            chroma_server_host=os.environ.get("CHROMA_HOST", "0.0.0.0"),
            chroma_server_http_port="8000",
        ),
        collection_name=collection_name if collection_name is not None else "confluence",
        # collection_metadata=chroma_db_settings.collection_metadata if chroma_db_settings.collection_metadata is not None else {"source": "Confluence / Jira"},
        persist_directory=persist_dir,
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        ))

    def create_documents(self, texts: list[str], metadatas: list[DocumentMetadata] = None):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, length_function=len
        )
        documents = text_splitter.create_documents(texts, metadatas)
        return documents

    
    def persist_state(self):
         self.db.persist()
    
    def store_documents(self, documents: List[Document]):
         print(documents)
         self.db.add_documents(documents)
    
    def reset_collection(self):
         self.db.delete_collection()

    def search_similarity(self, text: str, filters: Dict[str, str] = None):
        return self.db.similarity_search_with_score(query=text, k=5, filter=filters)