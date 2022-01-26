"""
A utility for navigating directory hierarchies on-disk.
"""

# Standard imports
import os


def sub_folder(folder_name: str) -> str:
    """
    Generates the absolute path to subfolder in the current working directory.

    :param folder_name: The name of the subfolder
    :return: The absolute pathname of the subfolder
    """

    subfolder = folder_name
    return up_path(__file__, 1) + '/' + subfolder


def up_path(path: str, n: int) -> str:
    """
    Function for traversing up n levels from the specified path.

    :param path: The absolute pathname of the directory
    :param n: The number of levels to traverse up the directory structure
    :return: The absolute pathname to the nth level-up directory
    """

    return os.sep.join(path.split(os.sep)[:-n])
    