import unittest

from confluence import load, iterate_spaces, iterate_latest_pages


class TestChromaUtils(unittest.TestCase):
    def test_load(self):
        documents = load(space_key="~637b97702acfad92d7b0ab23")
        print(documents)
        self.assertEqual(1, 1)


class TestFetchConfluence(unittest.TestCase):
    def test_get_spaces(self):
        spaces = iterate_spaces()
        print(spaces)
        self.assertEqual(1, 1)


class TestFetchConfluenceByCQL(unittest.TestCase):
    def test_exec_cql(self):
        spaces = iterate_latest_pages()
        print(spaces)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
