from pydantic import BaseModel, Field

class StatusSchema(BaseModel):
    name: str = Field(max_length=24)

class StatusInDBSchema(StatusSchema):
    id: int = Field(ge=1)