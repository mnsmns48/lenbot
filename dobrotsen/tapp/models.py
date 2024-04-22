from pydantic import BaseModel


class Menu(BaseModel):
    id: int
    parent: int
    title: str
    link: str | None
    price: float | None
    image: str | None
