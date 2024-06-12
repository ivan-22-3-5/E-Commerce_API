from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Float, Boolean, Enum, Table, Column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.custom_types import OrderStatus
from src.db.db import Base

product_category_association = Table(
    'product_category_association', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_name', String, ForeignKey('categories.name'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    refresh_token = relationship('RefreshToken', back_populates='user', uselist=False, cascade='all, delete')
    orders = relationship('Order', back_populates='user')
    reviews = relationship('Review', back_populates='user')
    addresses = relationship('Address', back_populates='user')
    cart = relationship('Cart', uselist=False)

    def __init__(self, email: str, password: str, username: str):
        self.email = email
        self.password = password
        self.username = username
        self.created_at = datetime.now()
        self.is_admin = False


class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    zipcode: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship('User', back_populates='addresses', uselist=False)


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship('User', back_populates='refresh_token', uselist=False)


class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    items = relationship('CartItem')

    @hybrid_property
    def total_price(self):
        return sum(item.total_price for item in self.items)


class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey('carts.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    product = relationship('Product', lazy="joined", uselist=False)

    @hybrid_property
    def total_price(self):
        return self.product.price * self.quantity

    def __init__(self, product_id: int, cart_id: int, quantity: int = 1):
        self.product_id = product_id
        self.cart_id = cart_id
        self.quantity = quantity


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'))

    user = relationship('User', back_populates='orders', uselist=False)
    product = relationship('Product', back_populates='orders', uselist=False)
    address = relationship('Address', uselist=False)

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

    orders = relationship('Order', back_populates='product', cascade='all, delete')
    categories = relationship('Category', back_populates='products', secondary=product_category_association)
    reviews = relationship('Review', back_populates='product')

    def __init__(self, title: str, description: str, price: float):
        self.title = title
        self.description = description
        self.price = price
        self.created_at = datetime.now()
        self.enabled = True


class Category(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    products = relationship('Product', back_populates='categories', secondary=product_category_association)

    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    product = relationship('Product', back_populates='reviews', uselist=False)
    user = relationship('User', back_populates='reviews', uselist=False)

    def __init__(self, user_id: int, product_id: int, rating: int, content: str):
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.content = content
        self.created_at = datetime.now()
