"""
Class which describes a spotify cookie which is necessary to authenticate a user
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (spotify_cookies.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################


class SpotifyCookies:
    """
    Class which describes a valid spotify cookie
    """

    def __init__(self, sp_t: str = None, sp_dc: str = None, sp_key: str = None):
        """
        Create a new spotify cookie. All values have to be set if you want to use it

        Args:
            sp_t: The name of the spotify cookie (Use the raw value of the cookie as value of this)
            sp_dc: The name of the spotify cookie (Use the raw value of the cookie as value of this)
            sp_key: The name of the spotify cookie (Use the raw value of the cookie as value of this)
        """
        self.sp_t: str = sp_t
        self.sp_dc: str = sp_dc
        self.sp_key: str = sp_key

    def validate(self) -> bool:
        """
        Check if all values are set correctly
        Returns:

        """
        if self.sp_t and self.sp_dc and self.sp_key:
            return True
        return False

    # TODO load from file
    # TODO load from env
