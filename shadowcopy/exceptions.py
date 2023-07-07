"""
Home to shadowcopy exceptions
"""


class RequiresAdminError(PermissionError):
    """
    Used to denote that this operation requires admin.. and we're not admin
    """

    pass


class OSUnsupportedError(OSError):
    """
    Used to denote that functionality is being used on an unsupported OS
    """

    pass


class PathIsNotToFile(FileNotFoundError):
    """
    Used to denote that src path is not a file
    """

    pass


class ShadowCopyFailure(OSError):
    """
    Generically used to denote that shadow copy failed
    """

    pass
