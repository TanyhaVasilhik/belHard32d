from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    category_id: int = Field(ge=1)
    price: float
    media: str = Field(max_length=24)
    total: int = Field(ge=1)
    is_published: bool
    name_en: str = Field(max_length=24)
    name: str = Field(max_length=24)

class ProductInDBSchema(ProductSchema):
    id: int = Field(ge=1)
