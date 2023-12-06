class ClientException(Exception):
    """
    Base class of all Client exceptions.
    """
    header_message = 'An unexpected client exception occured. More details:'

    def __init__(self, message='', *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        print(f'{self.header_message} {message}')
        raise self


class ClientExceptionInvalidArgument(ClientException):
    """
    Invalid argument.
    """
    header_message = 'Invalid UUID entered.'


class ClientExceptionFileNotFound(ClientException):
    """
    The File requested was not found.
    """
    header_message = 'File was not found on the remote server.'


class ClientExceptionFailedPrecondition(ClientException):
    """
    The remote service failed - it's database is not running.
    """
    header_message = 'The remote service failed.'


class ClientExceptionInvalidURL(ClientException):
    """
    Invalid URL.
    """
    header_message = 'Invalid URL was entered.'
