from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import BotUser, create_async_session, Product
from schemas import BotUserSchema, BotUserInDBSchema, ProductInDBSchema


class CRUDBotUser:

    @staticmethod
    @create_async_session
    async def add(bot_user: BotUserSchema, session: AsyncSession = None) -> BotUserInDBSchema | None:
        bot_user = BotUser(
            **bot_user.dict()
        )
        session.add(bot_user)
        try:
            await session.commit()
        except IntegrityError:
            return None
        else:
            await session.refresh(bot_user)
            return BotUserInDBSchema(**bot_user.__dict__)

    @staticmethod
    @create_async_session
    async def get(bot_user_id: int, session: AsyncSession = None) -> BotUserInDBSchema | None:
        bot_user = await session.execute(
            select(BotUser).where(BotUser.id == bot_user_id)
        )
        bot_user = bot_user.first()
        if bot_user:
            return BotUserInDBSchema(**bot_user[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(parent_id: int = None, session: AsyncSession = None) -> list[BotUserInDBSchema]:
        if parent_id:
            bot_users = await session.execute(
                select(BotUser).order_by(BotUser.id).where(BotUser.parent_id == parent_id)
            )
        else:
            bot_users = await session.execute(
                select(BotUser).order_by(BotUser.id)
            )
        return [BotUserInDBSchema(**bot_user[0].__dict__) for bot_user in bot_users]

    @staticmethod
    @create_async_session
    async def delete(bot_user_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(BotUser).where(BotUser.id == bot_user_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def update(
            bot_user: BotUserInDBSchema,
            session: AsyncSession = None
    ) -> None:
        await session.execute(
            update(BotUser).where(BotUser.id == bot_user.id).values(
                **bot_user.__dict__
            )
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get_products(
            bot_user_id: int = None,
            session: AsyncSession = None
    ) -> list[tuple[BotUserInDBSchema, ProductInDBSchema]] | None:
        if bot_user_id:
            response = await session.execute(
                select(BotUser, Product)
                .join(Product, BotUser.id == Product.bot_user_id)
                .where(BotUser.id == bot_user_id)
            )
            return [
                (
                    BotUserInDBSchema(**res[0].__dict__),
                    ProductInDBSchema(**res[1].__dict__)
                ) for res in response
            ]
        else:
            response = await session.execute(
                select(BotUser, Product)
                .join(Product, BotUser.id == Product.bot_user_id)
            )
            return [
                (
                    BotUserInDBSchema(**res[0].__dict__),
                    ProductInDBSchema(**res[1].__dict__)
                ) for res in response
            ]