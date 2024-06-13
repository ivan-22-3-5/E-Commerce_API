from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.base import ObjUpdate


class AddressBase(BaseModel):
    fullname: str
    country: str
    city: str
    street: str
    zipcode: int


class AddressIn(AddressBase):
    pass


class AddressOut(AddressBase):
    id: int


class AddressUpdate(ObjUpdate):
    fullname: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    zipcode: Optional[int] = Field(default=None)
