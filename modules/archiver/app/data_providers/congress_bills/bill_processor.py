import os
import requests

from pymongo.errors import DuplicateKeyError
# from ratelimit import limits, sleep_and_retry
from tenacity import (
    Retrying,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
)

from app.storage_connectors.mongo_db_dataset_controller import MongoDBDatasetController

# TODO: once this is finalized a bit more, i want to extract the minimum required functionality of
# of this class into a Abstract class that can be used for other data providers to enforce a common
# interface for the data provider classes
class BillProcessor(DataProvider):

    def __init__(self, api_key=None):
        self.mdbc = MongoDBDatasetController(
            "CongressDB", 
            ["CongressBill", "LatestAction"]
        )

        self.api_key = api_key or os.environ.get("CONGRESS_API_KEY")

    def process_bill(self, new_bill):
        # Extract the 'latestAction' from the new bill
        latest_action_data = new_bill.pop('latestAction')

        # Add the 'congress', 'number', and 'originChamberCode' to the 'latestAction'
        # This is the common index between the two collections (created in the migrations)
        latest_action_data.update({
            "congress": new_bill["congress"],
            "number": new_bill["number"],
            "originChamberCode": new_bill["originChamberCode"]
        })

        # Insert the 'latestAction' into the 'LatestAction' collection
        self.safe_insert(self.mdbc.collections['LatestAction'], latest_action_data)

        # Add the 'latestActionId' to the new bill
        new_bill['latestActionId'] = latest_action_data['_id']

        # Insert the new bill into the 'CongressBill' collection and eat any DuplicateKeyErrors
        self.safe_insert(self.mdbc.collections['CongressBill'], new_bill)

    @staticmethod
    def safe_insert(collection, data): 
        # TODO: move this to a util mixin
        try: 
            collection.insert_one(data)
        except DuplicateKeyError as e:
            print(e)
        
    
    # @sleep_and_retry
    # @limits(calls=5000, period=86400)  # API limit per day (86400 seconds)
    def fetch_bill_data(self):
        url = f"https://api.congress.gov/v3/bill?api_key={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching bill data: {response.status_code}")

    def run_with_circuit_breaker(self):
        # Define circuit breaker settings
        circuit_breaker = Retrying(
            stop=stop_after_attempt(3),  # Retry for a maximum of 3 attempts
            wait=wait_random_exponential(multiplier=1, max=10),  # Wait between retries with random exponential backoff
            retry=retry_if_exception_type(requests.exceptions.RequestException),  # Retry if RequestException occurs
        )

        # Call the fetch_bill_data method with circuit breaker
        with circuit_breaker:
            bill_data = self.fetch_bill_data()
            # Process the fetched bill data as needed
            self.process_bill(bill_data)
