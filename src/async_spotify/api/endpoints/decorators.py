"""
A file with a wrapper functions
"""
from functools import wraps
from typing import Tuple

from .objects import DecoratorInformationObject
from ..api_request_maker import ApiRequestHandler
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


def make_request(url: str, method: str):
    """
    Wrap a get function

    Args:
        url: The url that should be called
        method: The method that should be used to make the request

    Returns:
        The executable function
    """

    def outer_wrapper(function: callable) -> callable:
        """
        Return the wrapper function so the wrapper function can be called

        Args:
            function: The function that should be called

        Returns:
            The wrapped function
        """

        @wraps(function)
        async def wrapper(*args, **kwargs) -> dict:
            """
            The wrapper that wraps the function to get the function arguments

            Args:
                args: The args of the function
                kwargs: The keyword args of the function

            Returns:
                The result of the function
            """

            # Get the args from the original api function
            return_values: DecoratorInformationObject = await function(*args, **kwargs)

            # Get the params required for making the api call
            query_params: dict = return_values.arguments
            auth_token: SpotifyAuthorisationToken = return_values.auth_token
            api_request_handler: ApiRequestHandler = return_values.request_maker

            # Fill in the required url params
            updated_url, query_params = format_map(url, query_params)

            # Make the api request
            return await api_request_handler.make_request(method, updated_url, query_params, auth_token)

        return wrapper

    return outer_wrapper


def format_map(string: str, map_object: dict) -> Tuple[str, dict]:
    """
    Formats a string with the map keys and returns the formatted string and the map without the used keys

    Args:
        string: The string which should be formatted
        map_object: The map which should be used form formatting

    Returns:
        Tuple(the formatted string, the dict without the used values)s

    """

    for key in list(map_object.keys()):
        if '{' + key + '}' in string:
            string = string.format_map({f'{key}': map_object[key]})
            map_object.pop(key, None)

    return string, map_object
