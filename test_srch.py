import unittest
from unittest.mock import patch
from srch import SearchService

class TestSearchService(unittest.TestCase):
    @patch('srch.OpenAIService')
    @patch('srch.SearchClient')
    def test_vector_search(self, mock_search_client, mock_openai_service):
        # Mock the necessary dependencies
        mock_search_client.return_value.search.return_value = [
            {
                '@search.reranker_score': 0.8,
                'title': 'Sample Title',
                'content': 'Sample Content',
                'category': 'Sample Category'
            }
        ]
        mock_openai_service.return_value.get_embeddings.return_value = 'Sample Embeddings'

        # Create an instance of SearchService
        search_service = SearchService()

        # Define the input
        query = 'Sample Query'

        # Call the method
        output_data, execution_time = search_service.vector_search(query)

        # Assert the expected output
        expected_output_data = [
            {
                'Score': 0.8,
                'Source': 'Sample Title',
                'Content': 'Sample Content',
                'file': 'Sample Category'
            }
        ]
        self.assertEqual(output_data, expected_output_data)
        self.assertGreaterEqual(execution_time, 0)

if __name__ == '__main__':
    unittest.main()