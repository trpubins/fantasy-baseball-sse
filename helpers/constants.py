"""
Provides project-specific constant values useful to both the client and the server.
"""

# Standard imports
from enum import Enum
import json

# Local imports
from helpers.paths import up_path


# Below url shows that 'int' is necessary as first param to make this Enum JSON serializable
# https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json
class HttpStatus(int, Enum):
    """
    Enumeration for HTTP status codes.

    OK = 200

    NOT_FOUND = 404

    INTERNAL_SERVER_ERROR = 500
    """

    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


def get_server_addr() -> str:
    """
    Retrieve the server ip address.

    :return: The server ip address as a string.
    """    
    return addr


def get_server_port() -> str:
    """
    Retrieve the server port number.
    
    :return: The server port number as a string.
    """
    return port


# parse the network config file
NETWORK_CFG_PATH = up_path(__file__, 2) + f'/network_cfg.json'
"""Absolute path to the network config file."""

addr = ''
"""The server ip address."""

port = ''
"""The server port number."""

with open(NETWORK_CFG_PATH) as json_cfg:
    data = json.load(json_cfg)
    addr = data['address']
    port = data['port']
