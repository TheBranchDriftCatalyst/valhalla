from app.data_providers.congress_gov.api.endpoints.bill_api import BillApi
from app.data_providers.data_provider import DataProvider

class RecentBillsDataProcessor(DataProvider):

    def schedule(self):
        # ever 30 minutes
        return "*/31 * * * *"
    
    def __init__(self, api_key=None):
        super().__init__()
        
    
    def run(self):
        response = BillApi().get_recent_bills()
        
        if response.status_code == 200:
            for bill in response.json()["results"][0]["bills"]:
                print(bill)
        else:
            raise Exception(f"Error fetching bill data: {response.status_code}")

