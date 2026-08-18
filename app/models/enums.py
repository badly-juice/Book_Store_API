import enum


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
