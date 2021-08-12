class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserExistsException(Exception):
    pass


class DBUserNotExistsException(Exception):
    pass


class DBMessageNotExistsException(Exception):
    pass


class DBFileNotExistsException(Exception):
    pass


class DBMsgFileNotExistsException(Exception):
    pass


class DBResourceDeletedException(Exception):
    pass


class DBResourceOwnerException(Exception):
    pass
