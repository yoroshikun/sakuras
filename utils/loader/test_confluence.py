import unittest
from confluence import load

class TestChromaUtils(unittest.TestCase):
    def test_load(self):
        documents = load(space_key="~637b97702acfad92d7b0ab23")
        print(documents)
        self.assertEqual(1, 1)
        

if __name__ == '__main__':
    unittest.main()