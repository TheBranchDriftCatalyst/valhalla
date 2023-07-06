import pytest
from mongomock import MongoClient

from bill_processor import BillProcessor

@pytest.fixture
def bill_processor():
    uri = 'mongodb://localhost:27017'
    database_name = 'test_database'
    collection_name = 'test_collection'
    api_key = 'YOUR_API_KEY'
    api_limit_per_day = 1000  # Set the desired API limit per day

    # Create a BillProcessor instance for testing
    return BillProcessor(uri, database_name, collection_name, api_key, api_limit_per_day)

def test_process_bill_insert(bill_processor, mongomock):
    # Mock the API response
    api_response = {
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

    # Set up the mock database
    mongomock_client = MongoClient()
    mongomock_db = mongomock_client["test_database"]
    collection = mongomock_db["test_collection"]

    # Call the process_bill method
    bill_processor.process_bill(api_response)

    # Verify that the document was inserted
    result = collection.find_one({"congress": 117, "number": "3076", "originChamberCode": "H"})

    assert result is not None

def test_process_bill_update(bill_processor, mongomock):
    # Set up the mock database
    mongomock_client = MongoClient()
    mongomock_db = mongomock_client["test_database"]
    collection = mongomock_db["test_collection"]

    # Insert a document to be updated
    collection.insert_one({
        "congress": 117,
        "number": "3076",
        "originChamberCode": "H",
        "title": "Old Bill Title"
    })

    # Mock the API response
    api_response = {
        "congress": 117,
        "latestAction": {
            "actionDate": "2022-04-06",
            "text": "Became Public Law No: 117-108."
        },
        "number": "3076",
        "originChamber": "House",
        "originChamberCode": "H",
        "title": "New Bill Title",
        "type": "HR",
        "updateDate": "2022-09-29",
        "updateDateIncludingText": "2022-09-29T03:27:05Z",
        "url": "https://api.congress.gov/v3/bill/117/hr/3076?format=json"
    }

    # Call the process_bill method
    bill_processor.process_bill(api_response)

    # Verify that the document was updated
    result = collection.find_one({"congress": 117, "number": "3076", "originChamberCode": "H"})

    assert result is not None
    assert result["title"] == "New Bill Title"

if __name__ == '__main__':
    pytest.main()
