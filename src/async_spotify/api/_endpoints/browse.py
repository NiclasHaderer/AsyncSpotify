"""
Module with the browse endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (browser.py) is part of AsyncSpotify which is released under MIT.                     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Browse(Endpoint):
    """
    The browser endpoint of the api
    """

    async def get_new_releases(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get a List of New Releases

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/console/get-new-releases/](https://developer.spotify.com/console/get-new-releases/)

        Returns:
            A list of new releases
        """

        args = {**kwargs}
        response = await self.api_request_handler.make_request('GET', URLS.BROWSE.RELEASES, args, auth_token)
        return response

    async def get_featured_playlists(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get a List of Featured Playlists

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/console/get-featured-playlists/](https://developer.spotify.com/console/get-featured-playlists/)

        Returns:
            The featured playlists
        """

        args = {**kwargs}
        response = await self.api_request_handler.make_request('GET', URLS.BROWSE.FEATURED_PLAYLISTS, args, auth_token)
        return response

    async def get_categories(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get a List of Browse Categories

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/console/get-browse-categories/](https://developer.spotify.com/console/get-browse-categories/)

        Returns:
            The available categories
        """

        args = {**kwargs}
        response = await self.api_request_handler.make_request('GET', URLS.BROWSE.CATEGORY_LIST, args, auth_token)
        return response

    async def get_single_category(self, category_id: str, auth_token: SpotifyAuthorisationToken = None,
                                  **kwargs) -> dict:
        """
        Get a Single Browse Category

        Args:
            category_id: The category id of the category you want
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/console/get-browse-category/](https://developer.spotify.com/console/get-browse-category/)

        Returns:
            A single category
        """

        required_args = {"category_id": category_id}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.BROWSE.CATEGORY, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_category_playlists(self, category_id: str, auth_token: SpotifyAuthorisationToken = None,
                                     **kwargs) -> dict:
        """
        Get a Category's playlists

        Args:
            category_id: The category id of the category you want
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/console/get-category-playlists/](https://developer.spotify.com/console/get-category-playlists/)

        Returns:
            The playlists of a category
        """

        required_args = {"category_id": category_id}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.BROWSE.CATEGORY_PLAYLIST, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_recommendation_by_seed(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Recommendations Based on Seeds
        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/console/get-recommendations/](https://developer.spotify.com/console/get-recommendations/)

        Returns:
            The Available Genre Seeds
        """

        args = {**kwargs}
        response = await self.api_request_handler.make_request('GET', URLS.BROWSE.RECOMMENDATIONS, args, auth_token)
        return response

    async def get_genre_seeds(self, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get Available Genre Seeds

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory

        Notes:
            [https://developer.spotify.com/console/get-available-genre-seeds/](https://developer.spotify.com/console/get-available-genre-seeds/)

        Returns:
            List of Genres
        """

        return await self.api_request_handler.make_request('GET', URLS.BROWSE.GENRE_SEEDS, {}, auth_token)
