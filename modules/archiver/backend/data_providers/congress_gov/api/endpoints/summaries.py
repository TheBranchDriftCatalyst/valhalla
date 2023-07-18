from backend.data_providers.congress_gov.api.congress_api import CongressAPI


class Summaries(CongressAPI):
    
    def __init__(self):
        super().__init__()
    
    def get_summaries(self, congress=None, bill_type=None):
        """
        Returns bill data from the API. If congress, bill_type, and bill_number are specified,
        returns detailed information for a specified bill. Otherwise, returns a list of bills
        sorted by date of latest action.
        """
        url = self.build_url()
        return self.get(url)

    def build_url(self, congress=None, bill_type=None):
        """
        Returns summaries data from the API. If congress and bill_type are specified,
        returns a list of summaries filtered by congress and by bill type, sorted by date of last update.
        Otherwise, returns a list of summaries sorted by date of last update.
        """
        endpoint = "summaries"
        if congress:
            endpoint += f"/{congress}"
            if bill_type:
                endpoint += f"/{bill_type}"
        return endpoint
