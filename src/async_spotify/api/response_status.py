from .status_codes import STATUS_CODES


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

        if status_code in STATUS_CODES["OK"]:
            success = True
            message = STATUS_CODES["OK"][status_code]

        elif status_code in STATUS_CODES["REDIRECT"]:
            success = True
            message = STATUS_CODES["REDIRECT"][status_code]

        elif status_code in STATUS_CODES["CLIENT_ERROR"]:
            success = True
            message = STATUS_CODES["CLIENT_ERROR"][status_code]

        elif status_code in STATUS_CODES["SERVER_ERROR"]:
            success = True
            message = STATUS_CODES["SERVER_ERROR"][status_code]
        else:
            success = False
            message = "Unknown response code"

        self.code: int = status_code
        self.success: bool = success
        self.message: str = message
