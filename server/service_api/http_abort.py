"""Functions for a server to abort an HTTP session with a client.
"""

# Standard modules
import sys

# 3rd party modules
from flask_restful import abort

# Project modules
sys.path.append('../../')
from helpers.constants import HttpStatus


def abort_file_not_found(file_path: str):
    """Raises an HTTPException with status code: `404 Not Found`.

    Parameters
    ----------
    file_path : str
        The file path that was not found on the server.
    """
    abort(HttpStatus.NOT_FOUND, message=f'The resource does not exist: {file_path}')


def abort_cannot_read_csv(file_path: str):
    """Raises an HTTPException with status code: `500 Internal Server Error`.

    Parameters
    ----------
    file_path : str
        The file path that could not be parsed.
    """
    abort(HttpStatus.INTERNAL_SERVER_ERROR, message=f'The requested resource was unable to be read: {file_path}')
