from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import create_async_session, Product
from schemas import ProductSchema, ProductInDBSchema


class CRUDProduct:

    @staticmethod
    @create_async_session
    async def add(product: ProductSchema, session: AsyncSession = None) -> ProductInDBSchema | None:
        product = Product(
            **product.dict()
        )
        session.add(product)
        try:
            await session.commit()
        except IntegrityError:
            return None
        else:
            await session.refresh(product)
            return ProductInDBSchema(**product.__dict__)

    @staticmethod
    @create_async_session
    async def get(product_id: int, session: AsyncSession = None) -> ProductInDBSchema | None:
        product = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product.first()
        if product:
            return ProductInDBSchema(**product[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(category_id: int = None, session: AsyncSession = None) -> list[ProductInDBSchema] | None:
        if category_id:
            products = await session.execute(
                select(Product).where(Product.category_id == category_id)
            )
        else:
            products = await session.execute(
                select(Product)
            )
        return [ProductInDBSchema(**product[0].__dict__) for product in products]

    @staticmethod
    @create_async_session
    async def update(product: ProductInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(Product).where(Product.id == product.id).values(
                **product.dict()
            )
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def delete(product_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(Product).where(Product.id == product_id)
        )
        await session.commit()
