import unittest


class MyTestCase(unittest.TestCase):
    def test_can_connect_to_minio(self):
        S3StorageConnector("test_bucket")


if __name__ == "__main__":
    unittest.main()
