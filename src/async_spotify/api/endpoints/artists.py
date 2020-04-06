"""
Handle the requests to the artist endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (artists.py) is part of AsyncSpotify which is released under MIT.                     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from async_spotify.api.endpoints.endpoint import Endpoint


class Artists(Endpoint):
    """
    Wraps the spotify artist functions
    """

    def get_artist(self, artist_id: str):
        """
        Get the artist by id

        Args:
            artist_id: The artist id

        Note:
            https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/

        Returns:
            The json associated with the artist
        """
