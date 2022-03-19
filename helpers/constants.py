"""Provides project-specific constant values useful to both the client and the server.
"""

# Standard modules
from enum import Enum
import json
import sys

# Project modules
from helpers.paths import up_path


# Below url shows that 'int' is necessary as first param to make this Enum JSON serializable
# https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json
class HttpStatus(int, Enum):
    """Enumeration for HTTP status codes.

    Enumerations
    ------------
    - OK = 200

    - NOT_FOUND = 404

    - INTERNAL_SERVER_ERROR = 500
    """

    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


def get_server_addr() -> str:
    """Retrieves the server ip address.

    Returns
    -------
    str
        The server ip address.
    """    
    return addr


def get_server_port() -> str:
    """Retrieves the server port number.
    
    Returns
    -------
    str
        The server port number.
    """
    return port


# parse the network config file
NETWORK_CFG_PATH = up_path(__file__, 2) + f'/network_cfg.json'
"""Absolute path to the network config file."""

addr = str()
"""The server ip address."""

port = str()
"""The server port number."""

try:
    with open(NETWORK_CFG_PATH) as json_cfg:
        data = json.load(json_cfg)
        addr = str(data['address'])
        port = str(data['port'])
except Exception as e:
    print(e)
    sys.exit()
