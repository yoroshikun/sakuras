from langchain.document_loaders.confluence import ConfluenceLoader

loader = ConfluenceLoader(
        url="https://mercari.atlassian.net/wiki",
        username="",
        api_key=""
    )

def load(space_key: str, cql: str = None):
    documents = loader.load(space_key=space_key, include_attachments=True, cql=cql)
    return documents