class CustomBaseException(Exception):
    def __init__(self):
        self.status_code = 500  # Internal Server Error


class DatabaseConnectionException(CustomBaseException):
    def __init__(self):
        self.status_code = 503  # Service Unavailable


class DatabaseException(CustomBaseException):
    def __init__(self):
        self.status_code = 503  # Service Unavailable
