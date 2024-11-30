from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Map MongoDB `_id` to `id`
    name: str
    age: int
    address: Address
