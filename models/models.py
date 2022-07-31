from datetime import datetime
from sqlalchemy import (Column, SmallInteger, ForeignKey, VARCHAR, TIMESTAMP, DECIMAL, Boolean)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Category(Base):
    tablename: str = "categories"

    id = Column(SmallInteger, primary_key=True)
    parent_id = Column(SmallInteger, ForeignKey("categories.id", ondelete="CASCADE"))
    is_published = Column(Boolean, unique=False, default=True)
    name_en = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(20), nullable=False)


class Product(Base):
    tablename: str = "products"

    id = Column(SmallInteger, primary_key=True)
    category_id = Column(SmallInteger, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(8, 2), default=0)
    media = Column(VARCHAR(20), nullable=False)
    total = Column(SmallInteger)
    is_published = Column(Boolean, unique=False, default=True)
    name_en = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(24), nullable=False)


class OrderItem(Base):
    tablename: str = "order_items"

    id = Column(SmallInteger, primary_key=True)
    order_id = Column(SmallInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(SmallInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    total = Column(SmallInteger)


class Order(Base):
    tablename: str = "orders"

    id = Column(SmallInteger, primary_key=True)
    bot_user_id = Column(SmallInteger, ForeignKey("bot_users.id", ondelete="CASCADE"), nullable=False)
    date_create = Column(TIMESTAMP, default=datetime.now())
    status_id = Column(SmallInteger, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)
    invoice_id = Column(SmallInteger, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)


class Status(Base):
    tablename: str = "statues"

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(20), nullable=False)


class Invoice(Base):
    tablename: str = "invoices"

    id = Column(SmallInteger, primary_key=True)
    bot_user_id = Column(SmallInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    date_create = Column(TIMESTAMP, default=datetime.now())
    total = Column(SmallInteger)
    status_id = Column(SmallInteger, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)


class BotUser(Base):
    tablename: str = "bot_users"

    id = Column(SmallInteger, primary_key=True)
    is_blocked = Column(Boolean, unique=False, default=True)
    balance = Column(SmallInteger)
    language_id = Column(SmallInteger, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)


class Language(Base):
    tablename: str = "languages"

    id = Column(SmallInteger, primary_key=True)
    language_code = Column(VARCHAR(20), nullable=False)
