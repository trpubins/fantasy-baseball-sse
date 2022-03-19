"""A utility for navigating directory hierarchies on-disk.
"""

# Standard modules
import os


def get_sub_dir(dirname: str, sub_dirname: str) -> str:
    """Retrieve the absolute path of the sub-directory, which is at the same level
    as the specified directory.
    
    Parameters
    ----------
    dirname : str
        The name of the working directory.

    sub_dirname : str
        The name of the sub-directory.

    Returns
    -------
    str
        The absolute pathname to the sub-directory.
    """
    return os.path.abspath(os.path.join(os.path.dirname(dirname), sub_dirname))


def up_path(start_path: str, n: int = 1) -> str:
    """Traverse up n levels from the specified path.

    Parameters
    ----------
    start_path : str
        The absolute pathname of the directory from which to start.

    n : int, optional
        The number of levels to traverse up the directory structure.
        Default is `1`.
    
    Returns
    -------
    str
        The absolute pathname to the nth level-up directory
    """
    return os.path.abspath(os.sep.join(start_path.split(os.sep)[:-n]))
    