from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Document(BaseModel):
    text: str


class EmbeddingOptions(BaseModel):
    document: Document
    debug: bool = False
    save: bool = True


def mount_route(app):
    @app.post("/make_embedding")
    async def make_embedding(options: EmbeddingOptions):
        # Make embedding, optional saving and optional returning data
        return {"message": "Hello World"}