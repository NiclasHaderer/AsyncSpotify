"""
Handle the requests to the artist endpoint
"""

from async_spotify import API


class Artist:
    """
    Wraps the spotify artist functions
    """

    def __init__(self, api_object: API):
        """
        Create a new spotify artist query class which handles the queries concerning artists
        :param api_object: The api object the class is assigned to
        """

        self.api_object: API = api_object

    def get_artist(self, artist_id: str):
        """
        Get the artist by id
        :param artist_id: The artist id
        :return: The json associated with the artist
        """

        pass
