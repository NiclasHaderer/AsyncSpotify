"""
Collection of spotify api urls replace with str.format(id='test')
"""

BASE_URL: str = "https://api.spotify.com/v1"


# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (urls.py) is part of AsyncSpotify which is released under MIT.                        #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

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

        ONE: str = BASE_URL + "/albums/{id}"
        TRACKS: str = BASE_URL + "/albums/{id}/tracks"
        MULTIPLE: str = BASE_URL + "/albums"

    class ARTIST:
        """
        URLs concerning the artist
        """

        ONE: str = BASE_URL + "/artists/{id}"
        ALBUM: str = BASE_URL + "/artists/{id}/albums"
        TOP_TRACKS: str = BASE_URL + "/artists/{id}/top-tracks"
        SIMILAR_ARTISTS: str = BASE_URL + "/artists/{id}/related-artists"
        SEVERAL: str = BASE_URL + "/artists/"

    class BROWSE:
        """
        URLs concerning the browsing of artists and categories
        """

        GENRE_SEEDS: str = BASE_URL + "/recommendations/available-genre-seeds"
        CATEGORY: str = BASE_URL + "/browse/categories/{category_id}"
        CATEGORY_PLAYLIST: str = BASE_URL + "/browse/categories/{category_id}/playlists"
        CATEGORY_LIST: str = BASE_URL + "/browse/categories"
        FEATURED_PLAYLISTS: str = BASE_URL + "/browse/featured-playlists"
        RELEASES: str = BASE_URL + "/browse/new-releases"
        RECOMMENDATIONS: str = BASE_URL + "/recommendations"

    class EPISODES:
        """
        URLs concerning episodes
        """

        ONE: str = BASE_URL + "/episodes/{id}"
        MULTIPLE: str = BASE_URL + "/episodes"

    class FOLLOW:
        """
        URLs concerning the follow endpoint
        """

        CONTAINS: str = BASE_URL + "/me/following/contains"
        CONTAINS_PLAYLIST: str = BASE_URL + "/playlists/{playlist_id}/followers/contains"
        HUMAN: str = BASE_URL + "/me/following"
        PLAYLIST: str = BASE_URL + "/playlists/{playlist_id}/followers"
        FOLLOWING_ARTISTS: str = BASE_URL + "/me/following?type=artist"

    class LIBRARY:
        """
        URLs concerning the user library
        """

        CONTAINS_ALBUM: str = BASE_URL + "/me/albums/contains"
        CONTAINS_TRACK: str = BASE_URL + "/me/tracks/contains"
        CONTAINS_SHOWS: str = BASE_URL + "/me/shows/contains"

        ALBUMS: str = BASE_URL + "/me/albums"
        TRACKS: str = BASE_URL + "/me/tracks"
        SHOWS: str = BASE_URL + "/me/shows"

    class PERSONALIZATION:
        """
        URLs to get habits over the user
        """

        TOP: str = BASE_URL + "/me/top/{type}"

    class PLAYER:
        """
        URLs concerning the player
        """

        PLAYER: str = BASE_URL + "/me/player"
        QUEUE: str = BASE_URL + "/me/player/queue"
        DEVICES: str = BASE_URL + "/me/player/devices"
        RECENTLY: str = BASE_URL + "/me/player/recently-played"
        PLAYING: str = BASE_URL + "/me/player/currently-playing"

        PAUSE: str = BASE_URL + "/me/player/pause"
        SEEK: str = BASE_URL + "/me/player/seek"
        REPEAT: str = BASE_URL + "/me/player/repeat"
        VOLUME: str = BASE_URL + "/me/player/volume"
        NEXT: str = BASE_URL + "/me/player/next"
        PREVIOUS: str = BASE_URL + "/me/player/previous"
        PLAY: str = BASE_URL + "/me/player/play"
        SHUFFLE: str = BASE_URL + "/me/player/shuffle"

    class PLAYLIST:
        """
        URLs concerning the playlists
        """
        ADD_TRACKS: str = BASE_URL + "/playlists/{playlist_id}/tracks"
        ONE: str = BASE_URL + "/playlists/{playlist_id}"
        CREATE: str = BASE_URL + "/users/{user_id}/playlists"
        ME: str = BASE_URL + "/me/playlists"
        USER: str = BASE_URL + "/users/{user_id}/playlists"
        COVER: str = BASE_URL + "/playlists/{playlist_id}/images"
        TRACKS: str = BASE_URL + "/playlists/{playlist_id}/tracks"

    SEARCH: str = BASE_URL + "/search"

    class SHOWS:
        """
        URLs concerning shows
        """

        ONE: str = BASE_URL + "/shows/{id}"
        EPISODES: str = BASE_URL + "/shows/{id}/episodes"
        SEVERAL: str = BASE_URL + "/shows"

    class TRACKS:
        """
        URLs concerning tracks
        """

        ANALYZE: str = BASE_URL + "/audio-analysis/{id}"
        FEATURES: str = BASE_URL + "/audio-features/{id}"
        MULTI_FEATURES: str = BASE_URL + "/audio-features"
        SEVERAL: str = BASE_URL + "/tracks"
        ONE: str = BASE_URL + "/tracks/{id}"

    class USER:
        """
        URLs concerning a spotify user profile
        """
        ME: str = BASE_URL + "/me"
        USER: str = BASE_URL + "/users/{user_id}"
