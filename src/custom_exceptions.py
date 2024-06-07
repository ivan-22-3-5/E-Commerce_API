class ECommerceApiError(Exception):
    def __init__(self, message: str = "Service is not available", headers=None):
        self.message = message
        self.headers = headers
        super().__init__(self.message)


class ResourceDoesNotExistError(ECommerceApiError):
    pass


class ResourceAlreadyExistError(ECommerceApiError):
    pass


class NotEnoughRightsError(ECommerceApiError):
    pass


class InvalidTokenError(ECommerceApiError):
    pass


class InvalidCredentialsError(ECommerceApiError):
    pass