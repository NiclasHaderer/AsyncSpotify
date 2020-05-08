"""
Class which handles the error message the spotify exceptions use
"""


# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (_error_message.py) is part of AsyncSpotify which is released under MIT.              #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import Dict


class ErrorMessage(object):
    """The error message"""

    def __init__(self, status: int = 0, message: str = ''):
        """
        Create a Error message object which will be used internally by the spotify exceptions

        Args:
            status: The http status code (0 if not applicable)
            message: The error message
        """
        self.message = message
        self.status = status

    @property
    def __dict__(self) -> Dict[str, Dict[str, str]]:
        """
        Returns: The error message which can is used by the spotify exceptions
        """
        return {'error': {'status': self.status, 'message': self.message}}
