from datetime import datetime
from pydantic import BaseModel, Field

class OrderSchema(BaseModel):
    bot_user_id: int = Field(ge=1)
    data_created: datetime = Field(default=datetime.now())
    status_id: int = Field(ge=1)
    invoice_id: int = Field(ge=1)

class OrderInDBSchema(OrderSchema):
     id: int = Field(ge=1)
