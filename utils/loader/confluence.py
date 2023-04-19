import os
from langchain.document_loaders.confluence import ConfluenceLoader

username = os.environ.get("CONFLUENCE_USERNAME", "")
api_key = os.environ.get("CONFLUENCE_API_KEY", "")

loader = ConfluenceLoader(
        url="https://mercari.atlassian.net/wiki",
        username=str(username),
        api_key=str(api_key)
    )

def load(space_key: str, cql: str = None):
    documents = loader.load(space_key=space_key, include_attachments=True, cql=cql)
    return documents