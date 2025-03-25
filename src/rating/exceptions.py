class NotFoundError(Exception):
    """Raised when a resource is not found."""

class InvalidScoreError(Exception):
    """Raised when an invalid score is submitted."""

class PaginationError(Exception):
    """Raised for invalid pagination parameters."""