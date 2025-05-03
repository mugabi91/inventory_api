from typing import Optional
from pydantic import BaseModel,EmailStr, constr
from typing import Annotated

class UsersIn(BaseModel):
    userEmail: EmailStr
    userFullName: str
    user_pwd: Annotated[str, constr(min_length=8, max_length=64)]

class UsersResponseSchema(BaseModel):
    userEmail: str
    userFullName: str
    class Config:
        from_attributes=True

