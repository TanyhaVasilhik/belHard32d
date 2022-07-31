from fastapi import APIRouter, HTTPException, Query, Depends
from schemas import OrderSchema, OrderInDBSchema
from crud import CRUDOrder

order_router = APIRouter(
    prefix="/order"
)


async def check_order_id(order_id: int = Query(ge=1)) -> int:
    order = await CRUDOrder.get(order_id=order_id)
    if order:
        return order_id
    raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")


@order_router.get("/get", response_model=OrderInDBSchema, tags=["Order"])
async def get_order(order_id: int = Depends(check_order_id)):
    return await CRUDOrder.get(order_id=order_id)


@order_router.get("/all", response_model=list[OrderInDBSchema], tags=["Order"])
async def get_all_orders(order_id: int = Query(ge=1, default=None)):
    return await CRUDOrder.get_all(order_id=order_id)


@order_router.post("/add", response_model=OrderInDBSchema, tags=["Order"])
async def add_order(order: OrderSchema):
    return await CRUDOrder.add(order=order) or HTTPException(status_code=404, detail="Order is exist")


@order_router.delete("/del", tags=["Order"])
async def delete_order(order_id: int = Depends(check_order_id)):
    await CRUDOrder.delete(order_id=order_id)
    raise HTTPException(status_code=200, detail="Order was deleted")


@order_router.put("/update", tags=["Order"])
async def update_order(order: OrderInDBSchema):
    await CRUDOrder.update(order=order)
    raise HTTPException(status_code=200, detail="Order was updated")
