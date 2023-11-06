from pydantic import BaseModel


class Dynamic(BaseModel):
    x: float
    y: float
    vx: float
    vy: float
