from pydantic import BaseModel


class Errors(BaseModel):
    code: int
    message: str
    details: str
