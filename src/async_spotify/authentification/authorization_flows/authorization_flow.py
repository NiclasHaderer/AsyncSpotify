# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (authorization_flow.py) is part of AsyncSpotify which is released under MIT.          #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import os
from abc import ABC, abstractmethod


class AuthorizationFlow(ABC):

    @abstractmethod
    def load_from_env(self) -> None:
        pass

    @abstractmethod
    def load_from_docker_secret(self, base_dir: str) -> None:
        pass

    @abstractmethod
    def save_to_evn(self) -> None:
        pass

    @abstractmethod
    def valid(self) -> bool:
        pass

    @staticmethod
    def _get_docker_secret(name: str, secrets_dir: str, default=None) -> str:
        """
        Read the docker secret and return it

        Args:
            name: The name of the docker secret
            secrets_dir: The directory where the secrets are stored
            default: The default value if no secret is found

        Returns:
            The docker secret
        """

        # try to read from secret file
        try:
            with open(os.path.join(secrets_dir, name), 'r') as secret_file:
                return secret_file.read().strip()
        except IOError:
            return default

    def __eq__(self, other) -> bool:
        """
        Support for equal assertion

        Args:
            other: The other object the comparison is made to

        Returns:
            Is the content of the objects equal
        """
        return self.__dict__ == other.__dict__
