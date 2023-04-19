from langchain.document_loaders.confluence import ConfluenceLoader

loader = ConfluenceLoader(
        url="https://mercari.atlassian.net/wiki",
        username="drew@mercari.com",
        api_key="ATATT3xFfGF0D_RlKzM6Gw9jXQmNv-5CmTMoVRlgLZSaLP2KuP32AZG6lmuhN-vd1VUoOMfpSSxMz3bYC0ZCjU4CmqWo84zzlWSL0Wh_RpvHl9vled3t9hGynSB9UMiOZzWvxg_NAfktFBunTRGJiPisyf-P8sV3wusleregXPCP6t-2i-E3Ubg=3529ED2C"
    )

def load(space_key: str, cql: str = None):
    documents = loader.load(space_key=space_key, include_attachments=True, cql=cql)
    return documents