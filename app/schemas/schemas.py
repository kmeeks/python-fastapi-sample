

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    status: str | None = "pending"

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

class TodoOut(TodoCreate):
    id: int
    class Config:
        orm_mode = True
