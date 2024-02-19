import unittest
from unittest.mock import patch
from format import text_to_docs

class TestFormat(unittest.TestCase):
    def test_text_to_docs(self):
        # Define the input
        page_content = "This is a sample page content."

        # Call the function
        documents = text_to_docs(page_content)

        # Assert the expected output
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].page_content, page_content)

if __name__ == '__main__':
    unittest.main()