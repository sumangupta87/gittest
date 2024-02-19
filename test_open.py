import unittest
from unittest.mock import patch
from open import get_embeddings

class TestGetEmbeddings(unittest.TestCase):
    @patch('open.requests')
    def test_get_embeddings_success(self, mock_requests):
        # Mock the necessary objects
        mock_response = mock_requests.request.return_value
        mock_response.text = '{"data": [{"embedding": [1.0, 2.0, 3.0]}]}'

        # Call the function
        embeddings = get_embeddings("sample text")

        # Assert the expected calls were made
        mock_requests.request.assert_called_once_with(
            "POST",
            EMBEDDINGS_URL,
            headers={'Content-Type': CONTENT_TYPE, 'api-key': API_KEY},
            data='{"input": "sample text"}',
            verify=False
        )

        # Assert the expected output
        self.assertEqual(embeddings, [1.0, 2.0, 3.0])

    @patch('open.requests')
    def test_get_embeddings_failure(self, mock_requests):
        # Mock the necessary objects
        mock_requests.request.side_effect = Exception("Failed to generate embeddings")

        # Call the function
        embeddings = get_embeddings("sample text")

        # Assert the expected calls were made
        mock_requests.request.assert_called_once_with(
            "POST",
            EMBEDDINGS_URL,
            headers={'Content-Type': CONTENT_TYPE, 'api-key': API_KEY},
            data='{"input": "sample text"}',
            verify=False
        )

        # Assert the expected output
        self.assertIsNone(embeddings)

if __name__ == '__main__':
    unittest.main()