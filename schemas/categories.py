from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    parent_id: int = Field(default=None, ge=1)
    is_published: bool
    name_en: str = Field(max_length=24)
    name: str = Field(max_length=24)

class CategoryInDBSchema(CategorySchema):
    id: int = Field(ge=1)

