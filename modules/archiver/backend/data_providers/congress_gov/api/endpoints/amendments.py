# from backend.data_providers.congress_gov.api.congress_api import CongressAPI


# class Amendments(CongressAPI):
    
#     RELATED_ENTITIES = ['actions', 'cosponsors', 'amendments']
    
#     def __init__(self):
#         super().__init__()
    
#     def get_amendments(self, congress=None, amendment_type=None, amendment_number=None):
#         """
#         Returns amendment data from the API. If congress, amendment_type, and amendment_number are specified,
#         returns detailed information for a specified amendment. Otherwise, returns a list of amendments
#         sorted by date of latest action.
#         """
#         url = self.build_url(congress, amendment_type, amendment_number)
#         return self.get(url)
    
#     def build_url(self, congress=None, amendment_type=None, amendment_number=None, sub_entity=None):
#         endpoint = "amendment"
#         if congress:
#             endpoint += f"/{congress}"
#             if amendment_type:
#                 endpoint += f"/{amendment_type}"
#                 if amendment_number:
#                     endpoint += f"/{amendment_number}"
#                     if sub_entity and sub_entity in self.RELATED_ENTITIES:
#                         endpoint += f"/{sub_entity}" 
#         return self.get(endpoint)