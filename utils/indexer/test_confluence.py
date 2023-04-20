import unittest
from confluence import ConfluenceIndexer

class TestConfluenceIndexer(unittest.TestCase):
    def test_document_creation(self):
        print("hello")
        indexer = ConfluenceIndexer(True)
        print("hello")
        documents = indexer.create_documents(["test"])
        print(documents)
        indexer.store_documents(documents)
        indexer.reset_collection()
        self.assertEqual(5, 5)
        

if __name__ == '__main__':
    unittest.main()