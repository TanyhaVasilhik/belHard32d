from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Order, create_async_session
from schemas import OrderSchema, OrderInDBSchema


class CRUDOrder:

    @staticmethod
    @create_async_session
    async def add(order: OrderSchema, session: AsyncSession = None) -> OrderInDBSchema | None:
        order = Order(
            **order.dict()
        )
        session.add(order)
        try:
            await session.commit()
        except IntegrityError:
            return None
        else:
            await session.refresh(order)
            return OrderInDBSchema(**order.__dict__)

    @staticmethod
    @create_async_session
    async def get(order_id: int, session: AsyncSession = None) -> OrderInDBSchema | None:
        order = await session.execute(
            select(Order).where(Order.id == order_id)
        )
        order = order.first()
        if order:
            return OrderInDBSchema(**order[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(category_id: int = None, session: AsyncSession = None) -> list[OrderInDBSchema] | None:
        if category_id:
            orders = await session.execute(
                select(Order).where(Order.category_id == category_id)
            )
        else:
            orders = await session.execute(
                select(Order)
            )
        return [OrderInDBSchema(**order[0].__dict__) for order in orders]

    @staticmethod
    @create_async_session
    async def update(order: OrderInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(Order).where(Order.id == order.id).values(
                **order.dict()
            )
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def delete(order_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(Order).where(Order.id == order_id)
        )
        await session.commit()
