import unittest
from unittest.mock import MagicMock
from blob import write_to_blob

class TestFunctions(unittest.TestCase):
    def test_write_to_blob(self):
        # Mock the necessary objects
        blob_service_client = MagicMock()
        container_client = MagicMock()
        blob_service_client.get_container_client.return_value = container_client

        # Define the inputs
        outputjson = '{"key": "value"}'
        output_json_filename = "output.json"

        # Call the function
        write_to_blob(outputjson, output_json_filename)

        # Assert the expected calls were made
        blob_service_client.from_connection_string.assert_called_once_with(STORAGE_CONNECTION_STRING)
        blob_service_client.get_container_client.assert_called_once_with(OUTPUT_VECTOR_CONTAINER_NAME)
        container_client.upload_blob.assert_called_once_with(output_json_filename, outputjson, overwrite=True)

if __name__ == '__main__':
    unittest.main()