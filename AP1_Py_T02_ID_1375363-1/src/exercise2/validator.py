import os


def validate_save_path(raw_path: str) -> str | None:
    """
    Check that the path exists, is a directory, and is writable.

    Returns the absolute path on success, None on failure.
    """
    if not raw_path:
        return None

    path = os.path.abspath(os.path.expanduser(raw_path))

    if not os.path.exists(path):
        return None
    if not os.path.isdir(path):
        return None
    if not os.access(path, os.W_OK):
        return None

    return path