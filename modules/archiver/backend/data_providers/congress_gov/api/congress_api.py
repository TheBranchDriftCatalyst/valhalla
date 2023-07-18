import re
from os import environ
from pydantic import AnyHttpUrl, Json
import requests
from requests_ratelimiter import LimiterSession
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


class InvalidCongressAPILink(Exception):
    pass


class CongressAPI:
    # The comment is explaining that the `_rate_limiter` attribute is shared among all instances of
    # the CongressAPI class. This means that all instances of the class will use the same rate limiter
    # object to control the rate at which API requests are made. This ensures that the API requests do
    # not exceed the allowed rate limit.
    # this ratelimiter is used across all instances of the the congress api endpoints.
    # Extract this into a APIUtils Mixin class
    _rate_limiter = None

    @classmethod
    def get_ratelimiter(cls):
        """
        The function `get_ratelimiter` returns an instance of the `LimiterSession` class, creating it if
        it doesn't already exist.
        
        :return: The method is returning the `_rate_limiter` attribute of the `cls` class.
        """
        if cls._rate_limiter is None:
            cls._rate_limiter = LimiterSession(per_hour=1000)
        return cls._rate_limiter

    def __init__(
        self,
        base_url="https://api.congress.gov/v3",
        api_key=None,
        default_params=dict(limit=250),
    ):
        self.base_url = base_url
        self.api_key = environ.get("CONGRESS_API_KEY", api_key)
        # TODO: do not use url parameters, even if offered, use headers
        self.default_params = default_params
        self.rate_limiter = self.get_ratelimiter()
        # self.circuit_breaker = self.get_circuit_breaker()

    @retry(
        # Retry for a maximum of 3 attempts
        stop=stop_after_attempt(3),
        # Wait between retries with random exponential backoff
        wait=wait_random_exponential(multiplier=1, max=10), 
        # Retry if RequestException occurs
        retry=retry_if_exception_type(requests.exceptions.RequestException),
    )
    def get(self, endpoint, params=None) -> dict:
        """
        The function sends a GET request to an API endpoint with optional parameters and returns the
        JSON response.
        
        :param endpoint: The `endpoint` parameter is a string that represents the specific endpoint or
        URL path that you want to make a GET request to. It is appended to the `base_url` to form the
        complete URL for the request
        :param params: The `params` parameter is a dictionary that contains any additional query
        parameters that need to be included in the request URL. These parameters are used to filter or
        modify the response from the API
        :return: The method is returning the JSON response from the API call.
        """
        # Call the fetch_recent_bills method with circuit breaker
        # with self.circuit_breaker():
        response = self.rate_limiter.get(
            f"{self.base_url}/{endpoint}",
            params={**(params or {}), **self.default_params},
            headers={"x-api-key": self.api_key},
        )
        response.raise_for_status()
        return response.json()

    def follow_link(self, uri):
        """
        The `follow_link` function checks if a given URI matches the base URL and if so, it removes the
        base URL from the URI and makes a GET request to the modified URI. If the URI does not match the
        base URL, it raises an exception.
        
        :param uri: The `uri` parameter is a string that represents the URL that needs to be followed
        :return: The code is returning the result of the `get` method call.
        """
        pattern = re.compile(f"^/?{self.base_url}")
        if bool(pattern.match(uri)):
            return self.get(re.sub(pattern, "", uri))
        else:
            raise InvalidCongressAPILink(
                f"Trying to follow a url that doesn't appear to be a congress.gov url {uri}",
            )
