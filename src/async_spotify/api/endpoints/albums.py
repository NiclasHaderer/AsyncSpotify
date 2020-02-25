"""
Handle the requests to the albums endpoint
"""

from typing import List

import async_spotify


class Albums:
    """
    Wraps the spotify album functions
    """

    def __init__(self, api_object):
        """
        Create a new spotify album query class which handles the queries concerning albums

        Args:
            api_object: The api object the class is assigned to
        """

        self.api_object = api_object  # type: async_spotify.API

    async def get_album(self, album_id: str, **kwargs) -> dict:
        """
        Get the album with the specific spotify album id

        Args:
            album_id: The album id of the album you want to get
            kwargs: Optional arguments as keyword args

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-album/](https://developer.spotify.com/documentation/web-api/reference/albums/get-album/)

        Returns:
            The album json
        """

        required_args = {"id": album_id}
        return {**required_args, **kwargs}

    async def get_album_tracks(self, album_id: str) -> dict:
        """
        Get the tracks of an album

        Args:
            album_id: The id of the album

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/](https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/)

        Returns:
            The api response from spotify
        """
        pass

    async def get_multiple_albums(self, album_id_list: List[str]) -> dict:
        """
        Get All the albums specified in the album_id_list

        Args:
            album_id_list: The list of the spotify album ids

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-several-albums/](https://developer.spotify.com/documentation/web-api/reference/albums/get-several-albums/)

        Returns:
            The api response from spotify
        """
        pass
