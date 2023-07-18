# from backend.data_providers.congress_gov.api.congress_api import CongressAPI


# class Bills(CongressAPI):
    
#     RELATED_ENTITIES = ['actions', 'amendments', 'committees', 'cosponsors', 'relatedbills', 'subjects', 'summaries', 'text', 'titles']
    
#     def __init__(self):
#         super().__init__()
    
#     def get_recent_bills(self):
#         return self.get_bills()
    
#     def get_bills(self, congress=None, bill_type=None, bill_number=None, sub_entity=None):
#         """
#         Returns bill data from the API. If congress, bill_type, and bill_number are specified,
#         returns detailed information for a specified bill. Otherwise, returns a list of bills
#         sorted by date of latest action.
#         """
#         url = self.build_url(congress, bill_type, bill_number, sub_entity)
#         return self.get(url)
    
#     # def get_member(self, bioguide_id=None):
#     #     """
#     #     Returns member data from the API. If bioguide_id is specified,
#     #     returns detailed information for a specified congressional member. Otherwise, returns a list of
#     #     congressional members.
#     #     """
#     #     endpoint = "member"
#     #     if bioguide_id:
#     #         endpoint += f"/{bioguide_id}"
#     #     return self.get(endpoint)
