"""
Wraps the status code of a response to give some additional context
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (response_status.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from ._status_codes import STATUS_CODES


class ResponseStatus:
    """
    A response status object that can be checked if a request was ok
    """

    def __init__(self, status_code: int):
        """
        Create a Response status object that translates the status code to a success and message

        Args:
            status_code: A valid http status code
        """

        self.moved = False
        self.success = False
        self.error = False

        if status_code in STATUS_CODES["OK"]:
            self.success = True
            message: str = STATUS_CODES["OK"][status_code][0]

        elif status_code in STATUS_CODES["REDIRECT"]:
            self.moved = True
            message: str = STATUS_CODES["REDIRECT"][status_code][0]

        elif status_code in STATUS_CODES["CLIENT_ERROR"]:
            self.error = True
            message: str = STATUS_CODES["CLIENT_ERROR"][status_code][0]

        elif status_code in STATUS_CODES["SERVER_ERROR"]:
            self.error = True
            message = STATUS_CODES["SERVER_ERROR"][status_code][0]
        else:
            self.error = True
            message: str = "Unknown response code"

        self.code: int = status_code
        self.message: str = message
