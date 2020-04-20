"""Error messages"""


# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (_error_message.py) is part of AsyncSpotify which is released under MIT.              #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################


class ErrorMessage(object):
    """The error message"""

    def __init__(self, status: int = 0, message: str = ''):
        self.message = message
        self.status = status

    @property
    def __dict__(self) -> dict:
        return {'error': {'status': self.status, 'message': self.message}}
