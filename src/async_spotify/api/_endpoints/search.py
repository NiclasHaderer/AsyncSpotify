"""
Module with the search endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (search.py) is part of AsyncSpotify which is released under MIT.                      #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Search(Endpoint):
    """
    Search endpoint
    """

    async def start(self, query: str, query_type: List[str], auth_token: SpotifyAuthorisationToken = None,
                    **kwargs) -> dict:
        """
        Make a search

        Notes:
            https://developer.spotify.com/documentation/web-api/reference/search/search/

        Args:
            query: The search query
            query_type: A comma-separated list of item types to search across.
                Valid types are: album , artist, playlist, track, show and episode.
                Search results include hits from all the specified item types.
                For example: q=name:abacab&type=album,track returns both albums and tracks with
                “abacab” included in their name.
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The search result
        """

        args = {**{'q': query, 'type': query_type}, **kwargs}
        return await self.api_request_handler.make_request('GET', URLS.SEARCH, args, auth_token)
