import unittest
from pymongo import MongoClient
from data_providers.congress_bills.bill_processor import BillProcessor

class TestBillProcessor(unittest.TestCase):

    def test_process_bill(self):
        # Create a mock MongoDB client
        client = MongoClient()

        # Create an instance of your BillProcessor class
        bill_processor = BillProcessor(api_key="not_a_real_key")

        # Define a sample bill
        new_bill = {
            "congress": 117,
            "latestAction": {
                "actionDate": "2022-04-06",
                "text": "Became Public Law No: 117-108."
            },
            "number": "3076",
            "originChamber": "House",
            "originChamberCode": "H",
            "title": "Postal Service Reform Act of 2022",
            "type": "HR",
            "updateDate": "2022-09-29",
            "updateDateIncludingText": "2022-09-29T03:27:05Z",
            "url": "https://api.congress.gov/v3/bill/117/hr/3076?format=json"
        }

        # Call the method to test
        bill_processor.process_bill(new_bill)

        # Check that the bill was inserted into the 'CongressBill' collection
        self.assertIsNotNone(client['CongressDB']['CongressBill'].find_one({
            "congress": 117, "number": "3076", "originChamberCode": "H"
        }))

        # Check that the latest action was inserted into the 'LatestAction' collection
        self.assertIsNotNone(client['CongressDB']['LatestAction'].find_one({"actionDate": "2022-04-06", "text": "Became Public Law No: 117-108."}))

if __name__ == '__main__':
    unittest.main()
