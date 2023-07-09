from os import environ
import re
import requests
from requests_ratelimiter import LimiterSession
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

class InvalidCongressAPILink(Exception):
    pass


class CongressAPI:
    # this ratelimiter is used across all instances of the the congress api endpoints.
    # Extract this into a APIUtils Mixin class
    _rate_limiter = None
    _circuit_breaker = None

    @classmethod
    def get_ratelimiter(cls):
        if cls._rate_limiter is None:
            cls._rate_limiter = LimiterSession(per_hour=1000)
        return cls._rate_limiter

    @classmethod
    def get_circuit_breaker(cls):
        # Define circuit breaker settings
        if cls._circuit_breaker is None:
            cls._circuit_breaker = Retrying(
                stop=stop_after_attempt(3),  # Retry for a maximum of 3 attempts
                wait=wait_random_exponential(
                    multiplier=1, max=10
                ),  # Wait between retries with random exponential backoff
                retry=retry_if_exception_type(
                    requests.exceptions.RequestException
                ),  # Retry if RequestException occurs
            )
        return cls._circuit_breaker

    def __init__(
        self,
        base_url="https://api.congress.gov/v3",
        api_key=None,
        default_params=dict(limit=250),
    ):
        self.base_url = base_url
        self.api_key = environ.get("CONGRESS_API_KEY", api_key)

        default_params.setdefault("api_key", self.api_key)
        self.default_params = default_params
        self.rate_limiter = self.get_ratelimiter()
        self.circuit_breaker = self.get_circuit_breaker()

    def get(self, endpoint, params=None):
        # Call the fetch_recent_bills method with circuit breaker
        with self.circuit_breaker:
            response = self.rate_limiter.get(
                f"{self.base_url}/{endpoint}",
                params={**self.default_params, **(params or {})},
            )
            response.raise_for_status()
            return response.json()

    def follow_link(self, uri):
        """
        Returns data from the API for a specified uri.
        Useful for crawling around the response to get more data
        """
        pattern = re.compile(f"^/?{self.base_url}")
        if bool(pattern.match(uri)):
            return self.get(re.sub(pattern, "", uri))
        else:
            raise InvalidCongressAPILink(
                f"Trying to follow a url that doesn't appear to be a congress.gov url {uri}",
            )

    # def get_amendment(self, congress=None, amendment_type=None, amendment_number=None):
    #     """
    #     Returns amendment data from the API. If congress, amendment_type, and amendment_number are specified,
    #     returns detailed information for a specified amendment. Otherwise, returns a list of amendments
    #     sorted by date of latest action.
    #     """
    #     endpoint = "amendment"
    #     if congress:
    #         endpoint += f"/{congress}"
    #         if amendment_type:
    #             endpoint += f"/{amendment_type}"
    #             if amendment_number:
    #                 endpoint += f"/{amendment_number}"
    #     return self.get(endpoint)

    # def get_summaries(self, congress=None, bill_type=None):
    #     """
    #     Returns summaries data from the API. If congress and bill_type are specified,
    #     returns a list of summaries filtered by congress and by bill type, sorted by date of last update.
    #     Otherwise, returns a list of summaries sorted by date of last update.
    #     """
    #     endpoint = "summaries"
    #     if congress:
    #         endpoint += f"/{congress}"
    #         if bill_type:
    #             endpoint += f"/{bill_type}"
    #     return self.get(endpoint)

    # def get_congress(self, congress=None):
    #     """
    #     Returns congress and congressional sessions data from the API. If congress is specified,
    #     returns detailed information for a specified congress. Otherwise, returns a list of congresses
    #     and congressional sessions.
    #     """
    #     endpoint = "congress"
    #     if congress:
    #         endpoint += f"/{congress}"
    #     return self.get(endpoint)

    # def get_member(self, bioguide_id=None):
    #     """
    #     Returns member data from the API. If bioguide_id is specified,
    #     returns detailed information for a specified congressional member. Otherwise, returns a list of
    #     congressional members.
    #     """
    #     endpoint = "member"
    #     if bioguide_id:
    #         endpoint += f"/{bioguide_id}"
    #     return self.get(endpoint)

    # def get_committee(self, chamber=None, congress=None):
    #     """
    #     Returns committee data from the API. If chamber and congress are specified,
    #     returns a list of committees filtered by the specified congress and chamber. Otherwise, returns a list of
    #     congressional committees.
    #     """
    #     endpoint = "committee"
    #     if chamber:
    #         endpoint += f"/{chamber}"
    #         if congress:
    #             endpoint += f"/{congress}"
    #     return self.get(endpoint)

    # # Add similar methods for other endpoints
