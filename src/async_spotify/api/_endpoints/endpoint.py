"""
Abstract class which has to be extended by a endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (endpoint.py) is part of AsyncSpotify which is released under MIT.                    #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from abc import ABC
from typing import Tuple

from async_spotify.api._api_request_maker import ApiRequestHandler


class Endpoint(ABC):
    """
    Abstract class which has to be extended by a endpoint
    """

    def __init__(self, api_request_handler):
        """
        Create a new endpoint
        Args:
            api_request_handler: The api request handler form the main api class
        """
        self.api_request_handler: ApiRequestHandler = api_request_handler

    @staticmethod
    def _add_url_params(url_string: str, map_object: dict) -> Tuple[str, dict]:
        """
        Formats a string with the map keys and returns the formatted string and the map without the used keys

        Args:
            url_string: The string which should be formatted
            map_object: The map which should be used form formatting

        Returns:
            Tuple(the formatted string, the dict without the used values)s

        """

        return_url_string: str = url_string
        for key in list(map_object.keys()):
            if '{' + key + '}' in url_string:
                return_url_string = url_string.format_map({f'{key}': map_object[key]})
                map_object.pop(key, None)

        return return_url_string, map_object
