
from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    status: str | None = "pending"


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TodoOut(TodoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
