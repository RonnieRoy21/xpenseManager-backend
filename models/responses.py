from pydantic import BaseModel


class ResponseModel(BaseModel):
    message: str
    error: str | None = None
