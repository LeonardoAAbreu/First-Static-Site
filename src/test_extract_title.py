import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        matches = extract_title("# Hello")
        self.assertEqual("Hello", matches)
