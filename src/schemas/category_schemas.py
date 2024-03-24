from pydantic import BaseModel, ConfigDict
from typing import Optional


class GetCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_rus: str
    name_en: Optional[str] = None
    availability: bool
    deleted_flag: bool


class CreateCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name_rus: str
    availability: bool
