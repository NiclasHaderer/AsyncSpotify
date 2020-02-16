import os

root = os.path.abspath(os.sep)


def get_docker_secret(name, default=None, secrets_dir=os.path.join(root, 'var', 'run', 'secrets')) -> str:
    """
    Read the docker secret and return it
    :param name: The name of the docker secret
    :param default: The default value if no secret is found
    :param secrets_dir: The directory where the secrets are stored
    :returns: The docker secret
    """

    # try to read from secret file
    try:
        with open(os.path.join(secrets_dir, name), 'r') as secret_file:
            return secret_file.read().strip()
    except IOError as _:
        return default
