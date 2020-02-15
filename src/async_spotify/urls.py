BASE_URL: str = "https://api.spotify.com/v1"


class URLS:
    AUTHORIZE: str = "https://accounts.spotify.com/authorize"
    REFRESH: str = "https://accounts.spotify.com/api/token"

    class ALBUM:
        ONE: str = BASE_URL + "/v1/albums/{id}"
        TRACKS: str = BASE_URL + "/v1/albums/{id}/tracks"
        MULTIPLE: str = BASE_URL + "/v1/albums"

    class ARTIST:
        ONE: str = BASE_URL + "/v1/artists/{id}"
        ALBUM: str = BASE_URL + "/v1/artists/{id}/albums"
        TOP_TRACKS: str = BASE_URL + "/v1/artists/{id}/top-tracks"
        RELATE_ARTISTS: str = BASE_URL + "/v1/artists/{id}/related-artists"
        MULTIPLE: str = BASE_URL + "/v1/artists/{id}/artists"

    class BROWSE:
        CATEGORY: str = BASE_URL + "/v1/browse/categories/{category_id}"
        CATEGORY_PLAYLIST: str = BASE_URL + "/v1/browse/categories/{category_id}/playlists"
        CATEGORY_LIST: str = BASE_URL + "/v1/browse/categories"
        PLAYLISTS: str = BASE_URL + "/v1/browse/featured-playlists"
        RELEASES: str = BASE_URL + "/v1/browse/new-releases"
        RECOMMENDATIONS: str = BASE_URL + "/v1/recommendations"

    class FOLLOW:
        CONTAINS_ARTIST: str = BASE_URL + "/v1/me/following/contains"
        CONTAINS_PLAYLIST: str = BASE_URL + "/v1/playlists/{playlist_id}/followers/contains"
        HUMAN: str = BASE_URL + "/v1/me/following"
        PLAYLIST: str = BASE_URL + "/v1/playlists/{playlist_id}/followers"
        FOLLOWING_ARTISTS: str = BASE_URL + "/v1/me/following?type=artist"
