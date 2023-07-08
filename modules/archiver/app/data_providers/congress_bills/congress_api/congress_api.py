from os import environ
import re
import requests
from requests_ratelimiter import LimiterSession

class CongressAPI:
    def __init__(self, base_url="https://api.congress.gov/v3", api_key=None, default_params=dict(limit=250)):
        self.base_url = base_url
        self.api_key = environ.get("CONGRESS_API_KEY", api_key)
        
        default_params.setdefault("api_key", self.api_key)
        self.default_params = default_params
        self.rate_limiter = LimiterSession(per_hour=1000)

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params={**self.default_params, **(params or {})})
        response.raise_for_status()
        return response.json()

    def get_bill(self, congress=None, bill_type=None, bill_number=None, suffix=None):
        """
        Returns bill data from the API. If congress, bill_type, and bill_number are specified,
        returns detailed information for a specified bill. Otherwise, returns a list of bills
        sorted by date of latest action.
        """
        endpoint = "bill"
        
        if congress:
            endpoint += f"/{congress}"
            if bill_type:
                endpoint += f"/{bill_type}"
                if bill_number:
                    endpoint += f"/{bill_number}"
                    allowed_suffixes = ['actions', 'amendments', 'committees', 'cosponsors', 'relatedbills', 'subjects', 'summaries', 'text', 'titles']
                    if suffix and suffix in allowed_suffixes:
                        endpoint += f"/{suffix}"

        return self.get(endpoint)
    
    def follow_link(self, uri):
        """
        Returns data from the API for a specified uri.
        """
        pattern = re.compile(f'^/?{self.base_url}')
        if bool(pattern.match(uri)):
            return self.get(re.sub(pattern, '', uri))
        else:
            raise Exception(f"Trying to follow a url that doesn't appear to be a congress.gov url {uri}", )

    def get_amendment(self, congress=None, amendment_type=None, amendment_number=None):
        """
        Returns amendment data from the API. If congress, amendment_type, and amendment_number are specified,
        returns detailed information for a specified amendment. Otherwise, returns a list of amendments
        sorted by date of latest action.
        """
        endpoint = "amendment"
        if congress:
            endpoint += f"/{congress}"
            if amendment_type:
                endpoint += f"/{amendment_type}"
                if amendment_number:
                    endpoint += f"/{amendment_number}"
        return self.get(endpoint)

    def get_summaries(self, congress=None, bill_type=None):
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
        return self.get(endpoint)

    def get_congress(self, congress=None):
        """
        Returns congress and congressional sessions data from the API. If congress is specified,
        returns detailed information for a specified congress. Otherwise, returns a list of congresses
        and congressional sessions.
        """
        endpoint = "congress"
        if congress:
            endpoint += f"/{congress}"
        return self.get(endpoint)

    def get_member(self, bioguide_id=None):
        """
        Returns member data from the API. If bioguide_id is specified,
        returns detailed information for a specified congressional member. Otherwise, returns a list of
        congressional members.
        """
        endpoint = "member"
        if bioguide_id:
            endpoint += f"/{bioguide_id}"
        return self.get(endpoint)

    def get_committee(self, chamber=None, congress=None):
        """
        Returns committee data from the API. If chamber and congress are specified,
        returns a list of committees filtered by the specified congress and chamber. Otherwise, returns a list of
        congressional committees.
        """
        endpoint = "committee"
        if chamber:
            endpoint += f"/{chamber}"
            if congress:
                endpoint += f"/{congress}"
        return self.get(endpoint)

    # Add similar methods for other endpoints

api = CongressAPI()
print(api.get_bill(congress="116", bill_type="hr", bill_number="1"))
