from fastapi import status


class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail

        super().__init__(self.detail)


class UserNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found."


class UserAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists."


class InvalidCredentialsError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password."


class InvalidTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token."


class ExpiredTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has expired."


class BookNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Book not found."


class BookAlreadyExistsError(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Book already exists."


class OrderNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Order not found."


class OrderAlreadyCancelledError(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Order has already been cancelled."


class OrderCannotBeCancelledError(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Order cannot be cancelled."


class PermissionDeniedError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class CategoryNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Category not found"


class InsufficientStockError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Not enough books in stock"


class OrderModificationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Only pending orders can be modified"
