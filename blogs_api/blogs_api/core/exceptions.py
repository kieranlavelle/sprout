class APIException(Exception):
    """This exception is raised when the moderation service returns an error."""

    pass


class FailedToSaveBlogPost(Exception):
    """This exception is raised when the blog post could not be saved."""

    pass
