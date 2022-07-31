from fastapi import APIRouter, HTTPException, Query, Depends
from schemas import CategorySchema, CategoryInDBSchema
from crud import CRUDCategory

category_router = APIRouter(
    prefix="/category"
)


async def check_category_id(category_id: int = Query(ge=1)) -> int:
    category = await CRUDCategory.get(category_id=category_id)
    if category:
        return category_id
    raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")


@category_router.get("/get", response_model=CategoryInDBSchema, tags=["Category"])
async def get_category(category_id: int = Depends(check_category_id)):
    return await CRUDCategory.get(category_id=category_id)


@category_router.get("/all", response_model=list[CategoryInDBSchema], tags=["Category"])
async def get_all_categories(parent_id: int = Query(ge=1, default=None)):
    return await CRUDCategory.get_all(parent_id=parent_id)


@category_router.post("/add", response_model=CategoryInDBSchema, tags=["Category"])
async def add_category(category: CategorySchema):
    return await CRUDCategory.add(category=category) or HTTPException(status_code=404, detail="Category is exist")


@category_router.delete("/del", tags=["Category"])
async def delete_category(category_id: int = Depends(check_category_id)):
    await CRUDCategory.delete(category_id=category_id)
    raise HTTPException(status_code=200, detail="Category was deleted")


@category_router.put("/update", tags=["Category"])
async def update_category(category: CategoryInDBSchema):
    await CRUDCategory.update(category=category)
    raise HTTPException(status_code=200, detail="Category was updated")
