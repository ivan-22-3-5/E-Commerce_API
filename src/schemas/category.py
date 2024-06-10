from pydantic import BaseModel, field_validator


class CategoryIn(BaseModel):
    name: str

    @field_validator('name')
    def to_lower_case(cls, v):
        return v.lower()
