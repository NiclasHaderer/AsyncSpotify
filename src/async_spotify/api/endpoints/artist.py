"""
Handle the requests to the artist endpoint
"""
import async_spotify


class Artist:
    """
    Wraps the spotify artist functions
    """

    def __init__(self, api_object):
        """
        Create a new spotify artist query class which handles the queries concerning artists
        :param api_object: The api object the class is assigned to
        """

        self.api_object = api_object  # type: async_spotify.API

    def get_artist(self, artist_id: str):
        """
        Get the artist by id
        :param artist_id: The artist id
        :return: The json associated with the artist
        """

        pass
