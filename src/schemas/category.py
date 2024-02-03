from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class GetCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    availability: bool
    deleted_flag: bool
