"""
A file with a wrapper functions
"""
from functools import wraps

from ..api_request_maker import ApiRequestHandler
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken

api_request_handler = ApiRequestHandler()


def make_request(url: str, method: str):
    """
    Wrap a get function

    Args:
        method: The method that should be used to make the request
        url: The url that should be called

    Returns:
        The executable function
    """

    def outer_wrapper(function):
        """
        Return the wrapper function so the wrapper function can be called

        Args:
            function: The function that should be called

        Returns:
            The wrapped function
        """

        @wraps(function)
        async def wrapper(*args, **kwargs):
            """
            The wrapper that wraps the function to get the function arguments

            Args:
                args: The args of the function
                kwargs: The keyword args of the function

            Returns:
                The result of the function
            """

            # Get the args from the original api function
            return_values = function(*args, **kwargs)[0]
            query_params = return_values[0]
            auth_token: SpotifyAuthorisationToken = return_values[1]

            if method == "GET":
                response: dict = await api_request_handler.get_request(url, query_params, auth_token)

            if method == "PUT":
                response: dict = await api_request_handler.put_request(url, query_params, auth_token)

            return response

        return wrapper

    return outer_wrapper

# TODO save auth if token expired
