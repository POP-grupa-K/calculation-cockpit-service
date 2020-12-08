class NoSuchTaskException(Exception):
    pass


class TaskIsAlreadyRunningException(Exception):
    pass


class TaskIsAlreadyStoppedException(Exception):
    pass

class TaskAppNotAvailable(Exception):
    pass
