import os

def resolve_to_absolute_path(path: str) -> str:
    """
    Resolves a given path to an absolute path.

    Args:
        path (str): The path to resolve.

    Returns:
        str: The absolute path.
    """
    return os.path.abspath(path)