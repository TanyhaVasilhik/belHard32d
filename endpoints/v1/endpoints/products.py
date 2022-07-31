from fastapi import APIRouter, HTTPException, Query, Depends
from schemas import ProductSchema, ProductInDBSchema
from crud import CRUDProduct

product_router = APIRouter(
    prefix="/product"
)


async def check_product_id(product_id: int = Query(ge=1)) -> int:
    product = await CRUDProduct.get(product_id=product_id)
    if product:
        return product_id
    raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")


@product_router.get("/get", response_model=ProductInDBSchema, tags=["Product"])
async def get_product(product_id: int = Depends(check_product_id)):
    return await CRUDProduct.get(product_id=product_id)


@product_router.get("/all", response_model=list[ProductInDBSchema], tags=["Product"])
async def get_all_product(parent_id: int = Query(ge=1, default=None)):
    return await CRUDProduct.get_all(parent_id=parent_id)


@product_router.post("/add", response_model=ProductInDBSchema, tags=["Product"])
async def add_product(product: ProductSchema):
    return await CRUDProduct.add(product=product) or HTTPException(status_code=404, detail="Product is exist")


@product_router.delete("/del", tags=["Product"])
async def delete_product(product_id: int = Depends(check_product_id)):
    await CRUDProduct.delete(product_id=product_id)
    raise HTTPException(status_code=200, detail="Product was deleted")


@product_router.put("/update", tags=["Product"])
async def update_product(product: ProductInDBSchema):
    await CRUDProduct.update(product=product)
    raise HTTPException(status_code=200, detail="Product was updated")
