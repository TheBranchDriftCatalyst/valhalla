import requests
from ratelimit import limits, sleep_and_retry
from tenacity import (
    Retrying,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)

class BillProcessor:
    def __init__(self, uri, database_name, collection_name, api_key, api_limit_per_day):
        self.uri = uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.api_key = api_key
        self.api_limit_per_day = api_limit_per_day

    def process_bill(self, new_bill):
        # Connect to the MongoDB server
        client = MongoClient(self.uri)
        db = client[self.database_name]
        collection = db[self.collection_name]

        # Create the compound index if it doesn't exist
        collection.create_index(
            [("congress", 1), ("number", 1), ("originChamberCode", 1)],
            unique=True
        )

        # Upsert the bill with the latest action
        result = collection.update_one(
            {"congress": new_bill["congress"], "number": new_bill["number"], "originChamberCode": new_bill["originChamberCode"]},
            {"$set": {"latestAction": new_bill["latestAction"]}, "$setOnInsert": new_bill},
            upsert=True
        )

        if result.upserted_id is not None:
            print("New bill inserted")
        else:
            print("Existing bill updated with latest action")

        # Close the connection
        client.close()

    @sleep_and_retry
    @limits(calls=1, period=86400)  # API limit per day (86400 seconds)
    def fetch_bill_data(self):
        url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching bill data: {response.status_code}")

    def run_with_circuit_breaker(self):
        # Define circuit breaker settings
        retry_policy = Retrying(
            stop=stop_after_attempt(3),  # Retry for a maximum of 3 attempts
            wait=wait_random_exponential(multiplier=1, max=10),  # Wait between retries with random exponential backoff
            retry=retry_if_exception_type(requests.exceptions.RequestException),  # Retry if RequestException occurs
        )

        # Call the fetch_bill_data method with circuit breaker
        with retry_policy:
            bill_data = self.fetch_bill_data()
            # Process the fetched bill data as needed
            print(bill_data)    

# Usage example
uri = 'mongodb://localhost:27017'
database_name = 'mydatabase'
collection_name = 'bills'

bill_processor = BillProcessor(uri, database_name, collection_name)

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

bill_processor.process_bill(new_bill)
