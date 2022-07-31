from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Invoice, create_async_session, Product
from schemas import InvoiceSchema, InvoiceInDBSchema, ProductInDBSchema


class CRUDInvoice:

    @staticmethod
    @create_async_session
    async def add(invoice: InvoiceSchema, session: AsyncSession = None) -> InvoiceInDBSchema | None:
        invoice = Invoice(
            **invoice.dict()
        )
        session.add(invoice)
        try:
            await session.commit()
        except IntegrityError:
            return None
        else:
            await session.refresh(invoice)
            return InvoiceInDBSchema(**invoice.__dict__)

    @staticmethod
    @create_async_session
    async def get(invoice_id: int, session: AsyncSession = None) -> InvoiceInDBSchema | None:
        invoice = await session.execute(
            select(Invoice).where(Invoice.id == invoice_id)
        )
        invoice = invoice.first()
        if invoice:
            return InvoiceInDBSchema(**invoice[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(parent_id: int = None, session: AsyncSession = None) -> list[InvoiceInDBSchema]:
        if parent_id:
            invoices = await session.execute(
                select(Invoice).order_by(Invoice.id).where(Invoice.parent_id == parent_id)
            )
        else:
            invoices = await session.execute(
                select(Invoice).order_by(Invoice.id)
            )
        return [InvoiceInDBSchema(**invoice[0].__dict__) for invoice in invoices]

    @staticmethod
    @create_async_session
    async def delete(invoice_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(Invoice).where(Invoice.id == invoice_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def update(
            invoice: InvoiceInDBSchema,
            session: AsyncSession = None
    ) -> None:
        await session.execute(
            update(Invoice).where(Invoice.id == invoice.id).values(
                **invoice.__dict__
            )
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get_products(
            invoice_id: int = None,
            session: AsyncSession = None
    ) -> list[tuple[InvoiceInDBSchema, ProductInDBSchema]] | None:
        if invoice_id:
            response = await session.execute(
                select(Invoice, Product)
                .join(Product, Invoice.id == Product.invoice_id)
                .where(Invoice.id == invoice_id)
            )
            return [
                (
                    InvoiceInDBSchema(**res[0].__dict__),
                    ProductInDBSchema(**res[1].__dict__)
                ) for res in response
            ]
        else:
            response = await session.execute(
                select(Invoice, Product)
                .join(Product, Invoice.id == Product.invoice_id)
            )
            return [
                (
                    InvoiceInDBSchema(**res[0].__dict__),
                    ProductInDBSchema(**res[1].__dict__)
                ) for res in response
            ]