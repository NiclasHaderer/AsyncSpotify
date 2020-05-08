# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (token_renew_class.py) is part of AsyncSpotify which is released under MIT.           #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from .authentification.spotify_authorization_token import SpotifyAuthorisationToken


class TokenRenewClass:
    """
    Class which describes the interfaces the Token renew class has and can also be used to handle basic token renewal
    """

    async def __call__(self, spotify_api_client) -> SpotifyAuthorisationToken:
        """
        **Async** method which gets called if the token is expired

        Args:
            spotify_api_client: The instance of the [`SpotifyApiClient`][async_spotify.api.spotify_api_client]

        Returns: A renewed spotify authorization token
        """

        return await spotify_api_client.refresh_token()
