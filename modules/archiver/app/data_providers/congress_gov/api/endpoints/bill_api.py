from app.data_providers.congress_gov.api.congress_api import CongressAPI


class BillApi(CongressAPI):
    
    RELATED_ENTITIES = ['actions', 'amendments', 'committees', 'cosponsors', 'relatedbills', 'subjects', 'summaries', 'text', 'titles']
    
    def __init__(self):
        super().__init__()
    
    def get_recent_bills(self):
        return self.get_bills()
    
    def get_bills(self, congress=None, bill_type=None, bill_number=None, sub_entity=None):
        """
        Returns bill data from the API. If congress, bill_type, and bill_number are specified,
        returns detailed information for a specified bill. Otherwise, returns a list of bills
        sorted by date of latest action.
        """
        url = self.build_url(congress, bill_type, bill_number, sub_entity)
        return self.get(url)
    
    def build_url(self, congress=None, bill_type=None, bill_number=None, sub_entity=None):
        endpoint = "bill"
        if congress:
            endpoint += f"/{congress}"
            if bill_type:
                endpoint += f"/{bill_type}"
                if bill_number:
                    endpoint += f"/{bill_number}"
                    if sub_entity and sub_entity in self.RELATED_ENTITIES:
                        endpoint += f"/{sub_entity}" 
        return endpoint