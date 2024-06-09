from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.custom_types import OrderStatus
from src.db.db import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    refresh_token = relationship('RefreshToken', back_populates='user')
    orders = relationship('Order', back_populates='user')

    def __init__(self, email: str, password: str, username: str):
        self.email = email
        self.password = password
        self.username = username
        self.created_at = datetime.now()
        self.is_admin = False


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship('User', back_populates='refresh_token')


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))

    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

    def __init__(self, user_id: int, product_id: int):
        self.created_at = datetime.now()
        self.status = OrderStatus.PENDING
        self.user_id = user_id
        self.product_id = product_id


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)

    orders = relationship('Order', back_populates='product', cascade="all, delete")

    def __init__(self, title: str, description: str, price: float):
        self.title = title
        self.description = description
        self.price = price
        self.created_at = datetime.now()
        self.enabled = True
