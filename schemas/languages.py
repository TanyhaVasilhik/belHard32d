from pydantic import BaseModel, Field

class LanguageSchema(BaseModel):
    balance: int = Field(ge=0)
    language_id: int = Field(ge=1)

class LanguageInDBSchema(LanguageSchema):
    id: int = Field(ge=1)

