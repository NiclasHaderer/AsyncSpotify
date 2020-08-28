# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (authorization_flow.py) is part of AsyncSpotify which is released under MIT.          #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import os
from abc import ABC, abstractmethod
from os.path import join, abspath
from typing import Any, List


class AuthorizationFlow(ABC):
    """
    Abstract class which every auth flow should extend.
    Provides the basic features every auth flow should have.
    """

    def load_from_env(self) -> None:
        """
        Load the instance variables of the flow from the environment variables
        """
        for key in self._get_instance_variables():
            value = os.environ.get(key, self[key])
            if value and key == "scopes":
                value = value.split(" ")
            self[key] = value

    def load_from_docker_secret(self, base_dir: str = join(abspath(os.sep), 'var', 'run', 'secrets')) -> None:
        """
        Load the instance variables of the flow from docker secrets
        """
        for key in self._get_instance_variables():
            value = AuthorizationFlow._get_docker_secret(name=key, secrets_dir=base_dir, default=self[key])
            if value and key == "scopes":
                value = value.split(" ")
            self[key] = value

    def save_to_env(self) -> None:
        """
        Save the instance variables of the flow as environment variables
        """
        for key in self._get_instance_variables():
            value = self[key]
            if value:
                if isinstance(value, List):
                    value = " ".join(value)
                os.environ[key] = value

    @abstractmethod
    def valid(self) -> bool:
        """Check if the flow is valid"""

    def _get_instance_variables(self) -> [str]:
        """
        Get the instance variables keys

        Returns:
            The keys in a list
        """
        return self.__dict__.keys()

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

    def __getitem__(self, item) -> Any:
        if item not in self.__dict__:
            raise KeyError()
        return getattr(self, item)

    def __setitem__(self, key, value) -> None:
        if key not in self.__dict__:
            raise KeyError()
        setattr(self, key, value)

    def __eq__(self, other) -> bool:
        """
        Support for equal assertion

        Args:
            other: The other object the comparison is made to

        Returns:
            Is the content of the objects equal
        """
        return self.__dict__ == other.__dict__
