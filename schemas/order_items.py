from pydantic import BaseModel, Field

class OrderItemSchema(BaseModel):
    order_id: int = Field(ge=1)
    product_id: int = Field(ge=1)
    total: int = Field(ge=1)

class OrderItemInDBSchema(OrderItemSchema):
    id: int = Field(ge=1)
