# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (client_credentials_flow.py) is part of AsyncSpotify which is released under MIT.     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from .authorization_flow import AuthorizationFlow


class ClientCredentialsFlow(AuthorizationFlow):
    """
    Class which should be used for the Client credentials flow
    """

    def __init__(self, application_id: str = None, application_secret: str = None, ):
        """
        Create a new Spotify AuthorizationCodeFlow Object

        Args:
            application_id: The id of the application
            application_secret: The secret of the application
        """

        self.application_id: str = application_id
        self.application_secret: str = application_secret

    @property
    def valid(self) -> bool:
        """
        Check if the ClientCredentialsFlow is valid
        Returns: boolean
        """
        if self.application_id and self.application_secret:
            return True
        return False
