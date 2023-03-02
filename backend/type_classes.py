from pydantic import BaseModel


class InputArgs(BaseModel):
    inputType: str
    text: str
