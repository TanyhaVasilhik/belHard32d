from fastapi import APIRouter, HTTPException, Query, Depends
from schemas import OrderItemSchema, OrderItemInDBSchema
from crud import CRUDOrderItem

order_item_router = APIRouter(
    prefix="/order_item"
)


async def check_order_item_id(order_item_id: int = Query(ge=1)) -> int:
    order_item = await CRUDOrderItem.get(order_item_id=order_item_id)
    if order_item:
        return order_item_id
    raise HTTPException(status_code=404, detail=f"Order_item with id {order_item_id} not found")


@order_item_router.get("/get", response_model=OrderItemInDBSchema, tags=["Order_item"])
async def get_order_item(order_item_id: int = Depends(check_order_item_id)):
    return await CRUDOrderItem.get(order_item_id=order_item_id)


@order_item_router.get("/all", response_model=list[OrderItemInDBSchema], tags=["Order_item"])
async def get_all_order_items(parent_id: int = Query(ge=1, default=None)):
    return await CRUDOrderItem.get_all(parent_id=parent_id)


@order_item_router.post("/add", response_model=OrderItemInDBSchema, tags=["Order_item"])
async def add_order_item(order_item: OrderItemSchema):
    return await CRUDOrderItem.add(order_item=order_item) or HTTPException(status_code=404,
                                                                           detail="Order_item is exist")


@order_item_router.delete("/del", tags=["Order_item"])
async def delete_order_item(order_item_id: int = Depends(check_order_item_id)):
    await CRUDOrderItem.delete(order_item_id=order_item_id)
    raise HTTPException(status_code=200, detail="Order_item was deleted")


@order_item_router.put("/update", tags=["Order_item"])
async def update_order_item(order_item: OrderItemInDBSchema):
    await CRUDOrderItem.update(order_item=order_item)
    raise HTTPException(status_code=200, detail="Order_item was updated")
