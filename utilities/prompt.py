from pydantic import BaseModel


class Prompt(BaseModel):
    message:str
    model:str