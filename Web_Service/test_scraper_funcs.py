import unittest
from gnews import GNews
from scraper_funcs import create_search_string, create_instance, search, analysis_sentiment


class TestScraperFunciton(unittest.TestCase):
    def test_create_string(self):
        search_term = 'boris'
        blank_search_term = ''
        blocked_words = ['brexit', 'leadership']
        blocked_numbers = [42, 3.141]
        q01_search_term = create_search_string(search_term, blocked_words)
        q02_search_term = create_search_string(search_term, blocked_numbers)
        

        self.assertEqual(q01_search_term, 'boris -brexit -leadership')
        self.assertEqual(q02_search_term, 'boris -42 -3.141')
        with self.assertRaises(Exception):
            create_search_string(blank_search_term, blocked_numbers)
    
    def test_create_instance(self):
        gnews_obj = create_instance()
        self.assertEqual(type(gnews_obj), GNews)
    
    def test_search(self):
        gnews_obj_01 = create_instance()
        gnews_obj_02 = create_instance()
        search_term_01 = create_search_string('boris', [])
        search_term_02 = create_search_string('alskdjf', [])
        search_results = search(search_term_01, gnews_obj_01)
        search_length = len(search_results)

        self.assertGreater(search_length, 0)
        with self.assertRaises(Exception):
            search_results = search(search_term_02, gnews_obj_02)


if __name__ == "__main__":
    unittest.main()
