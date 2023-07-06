import unittest
from unittest.mock import MagicMock

class TestRecord(unittest.TestCase):
    def test_save_data(self):
        my_service = MyService("my_db")
        my_service.db = MagicMock()
        my_service.save_data("test data")
        my_service.db.connect.assert_called_once()
        my_service.db.insert.assert_called_once_with("test data")

if __name__ == '__main__':
    unittest.main()
