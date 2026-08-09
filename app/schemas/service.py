from typing import Optional

from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(
        default=None,
        max_length=500,
    )
    category: str = Field(..., min_length=2, max_length=100)
    duration: int = Field(..., gt=0, le=1440)
    price: float = Field(..., gt=0)


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
    )
    category: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    duration: Optional[int] = Field(
        default=None,
        gt=0,
        le=1440,
    )
    price: Optional[float] = Field(
        default=None,
        gt=0,
    )
    status: Optional[bool] = None


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    duration: int
    price: float
    status: bool
    provider_id: int

    class Config:
        from_attributes = True