"""
Collection of spotify api urls replace with str.format(id='test')
"""

BASE_URL: str = "https://api.spotify.com/v1"


class URLS:
    """
    Collection of spotify api urls
    """

    AUTHORIZE: str = "https://accounts.spotify.com/authorize"
    REFRESH: str = "https://accounts.spotify.com/api/token"

    class ALBUM:
        """
        URLs concerning the album
        """

        ONE: str = BASE_URL + "/v1/albums/{id}"
        TRACKS: str = BASE_URL + "/v1/albums/{id}/tracks"
        MULTIPLE: str = BASE_URL + "/v1/albums"

    class ARTIST:
        """
        URLs concerning the artist
        """

        ONE: str = BASE_URL + "/v1/artists/{id}"
        ALBUM: str = BASE_URL + "/v1/artists/{id}/albums"
        TOP_TRACKS: str = BASE_URL + "/v1/artists/{id}/top-tracks"
        RELATE_ARTISTS: str = BASE_URL + "/v1/artists/{id}/related-artists"
        MULTIPLE: str = BASE_URL + "/v1/artists/{id}/artists"

    class BROWSE:
        """
        URLs concerning the browsing of artists and categories
        """

        CATEGORY: str = BASE_URL + "/v1/browse/categories/{category_id}"
        CATEGORY_PLAYLIST: str = BASE_URL + "/v1/browse/categories/{category_id}/playlists"
        CATEGORY_LIST: str = BASE_URL + "/v1/browse/categories"
        PLAYLISTS: str = BASE_URL + "/v1/browse/featured-playlists"
        RELEASES: str = BASE_URL + "/v1/browse/new-releases"
        RECOMMENDATIONS: str = BASE_URL + "/v1/recommendations"

    class FOLLOW:
        """
        URLs concerning the follow endpoint
        """

        CONTAINS_ARTIST: str = BASE_URL + "/v1/me/following/contains"
        CONTAINS_PLAYLIST: str = BASE_URL + "/v1/playlists/{playlist_id}/followers/contains"
        HUMAN: str = BASE_URL + "/v1/me/following"
        PLAYLIST: str = BASE_URL + "/v1/playlists/{playlist_id}/followers"
        FOLLOWING_ARTISTS: str = BASE_URL + "/v1/me/following?type=artist"

    class LIBRARY:
        """
        URLs concerning the user library
        """

        SAVED_ALBUM: str = BASE_URL + "/v1/me/albums/contains"
        SAVED_TRACK: str = BASE_URL + "/v1/me/tracks/contains"
        USER_ALBUMS: str = BASE_URL + "/v1/me/albums"
        USER_TRACKS: str = BASE_URL + "/v1/me/tracks"
        REMOVE_SAVE_ALBUM: str = BASE_URL + "/v1/me/albums?ids={ids}"
        REMOVE_TRACK: str = BASE_URL + "/v1/me/albums/contains"

    class PERSONALIZATION:
        """
        URLs to get habits over the user
        """

        TOP: str = BASE_URL + "/v1/me/top/{type}"
