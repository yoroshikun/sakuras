import unittest
from .chroma import generate_embedding, init_collection

class TestChromaUtils(unittest.TestCase):
    def test_embedding_creation(self):
        result = generate_embedding("Hello world!")
        self.assertEqual(result, 5)
        
    def test_(self):
       result = init_collection("test")
       self.assertEqual() 

if __name__ == '__main__':
    unittest.main()