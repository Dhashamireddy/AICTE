class NotFoundError(Exception):
    """Raised by services when something does not exist. main.py turns it into HTTP 404."""

    def __init__(self, what: str):
        self.what = what
        super().__init__(f"{what} not found")


class ConflictError(Exception):
    """Raised when an action clashes with existing data. main.py turns it into HTTP 409."""