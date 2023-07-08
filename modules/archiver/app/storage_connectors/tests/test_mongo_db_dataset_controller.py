import unittest
from unittest.mock import patch, MagicMock
import unittest
from pymongo import MongoClient

class DBTest(unittest.TestCase):
    def setUp(self):
        """This method is called before each test."""
        pass  # If there's any setup to do before each test, do it here
    
    def tearDown(self):
        """This method is called after each test."""
        pass  # If there's any cleanup to do after each test, do it here

class TestMongoDBDatasetController(unittest.TestCase):
    def test_init(self):
        # Create a mock MongoDB client
        MongoDBDatasetController('test_dataset', ['collection1', 'collection2'])
#         # Define a sample bill
#         new_bill = {
#             "congress": 117,
#             "latestAction": {
#                 "actionDate": "2022-04-06",
#                 "text": "Became Public Law No: 117-108."
#             },
#             "number": "3076",
#             "originChamber": "House",
#             "originChamberCode": "H",
#             "title": "Postal Service Reform Act of 2022",
#             "type": "HR",
#             "updateDate": "2022-09-29",
#             "updateDateIncludingText": "2022-09-29T03:27:05Z",
#             "url": "https://api.congress.gov/v3/bill/117/hr/3076?format=json"
#         }

#         # Call the method to test
#         bp = BillProcessor(api_key="not_a_real_key")
#         bp.process_bill(new_bill)
        
#         # bp.mdbc.collections['CongressDB'][]
        
#         # Check that the bill was inserted into the 'CongressBill' collection
#         self.assertIsNotNone(bp.mdbc.collections['CongressBill'].find_one({
#             "congress": 117, "number": "3076", "originChamberCode": "H"
#         }))

#         # Check that the latest action was inserted into the 'LatestAction' collection
#         self.assertIsNotNone(bp.mdbc.collections['LatestAction'].find_one({
#             "actionDate": "2022-04-06", "text": "Became Public Law No: 117-108."}))

# if __name__ == '__main__':
#     unittest.main()

    
if __name__ == '__main__':
    unittest.main()
