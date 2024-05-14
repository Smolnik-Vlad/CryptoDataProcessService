class CustomBaseException(Exception):
    def __init__(self):
        self.status_code = 500  # Internal Server Error


class DatabaseConnectionException(CustomBaseException):
    def __init__(self):
        self.status_code = 503  # Service Unavailable


class DatabaseException(CustomBaseException):
    def __init__(self):
        self.status_code = 503  # Service Unavailable


class BadRequestException(CustomBaseException):
    def __init__(self):
        self.status_code = 400


class UnauthorizedAccessException(CustomBaseException):
    def __init__(self):
        self.status_code = 401


class TokenValidationErrorException(CustomBaseException):
    def __init__(self):
        self.status_code = 403


class ResourceIsForbiddenException(CustomBaseException):

    def __init__(self):
        self.status_code = 403


class NoSuchElementException(CustomBaseException):
    def __init__(self):
        self.status_code = 404


class ResourceNotFoundException(CustomBaseException):
    def __init__(self):
        self.status_code = 404


class MethodNotAllowedException(CustomBaseException):
    def __init__(self):
        self.status_code = 405


class RequestTimeoutException(CustomBaseException):
    def __init__(self):
        self.status_code = 408


class RequestAvailableException(CustomBaseException):
    def __init__(self):
        self.status_code = 502


class ConnectionErrorException(CustomBaseException):
    def __init__(self):
        self.status_code = 502


class TheServerIsFailedException(CustomBaseException):
    def __init__(self):
        self.status_code = 418


class WrongConnection400_500_Exception(CustomBaseException):
    def __init__(self):
        self.status_code = 418


class WrongConnection500_Exception(CustomBaseException):
    def __init__(self):
        self.status_code = 418
