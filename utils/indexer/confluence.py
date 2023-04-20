from indexer import Indexer, CollectionMetadata


class ConfluenceIndexer(Indexer):
    def __init__(self, isTest = False):
        super().__init__(collection_name="confluence" if isTest is False else "confluence-test", metadata=CollectionMetadata("documents"), chroma_db_settings=None)
