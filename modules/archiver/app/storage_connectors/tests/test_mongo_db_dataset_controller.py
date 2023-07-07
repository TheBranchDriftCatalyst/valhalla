import unittest
from unittest.mock import patch, MagicMock
from your_module import MongoDBDatasetController  # replace with the actual module name

class TestMongoDBDatasetController(unittest.TestCase):

    @patch('pymongo.MongoClient')
    def test_init(self, mock_client):
        # Mock the MongoClient
        mock_db = MagicMock()
        mock_client.return_value = mock_db

        # Define the dataset collections
        dataset_collections = ['collection1', 'collection2']

        # Create an instance of MongoDBDatasetController
        controller = MongoDBDatasetController('test_env', 'test_dataset', dataset_collections)

        # Check that the MongoClient was called with the correct arguments
        mock_client.assert_called_once_with('mongodb://localhost:27017/test_env')

        # Check that the collections attribute is correctly initialized
        expected_collections = {name: mock_db[name] for name in dataset_collections}
        self.assertEqual(controller.collections, expected_collections)

if __name__ == '__main__':
    unittest.main()
