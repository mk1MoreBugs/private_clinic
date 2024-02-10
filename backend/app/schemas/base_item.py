from pydantic import BaseModel


class BaseItem(BaseModel):
    id: int
    name: str
