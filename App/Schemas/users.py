
from pydantic import BaseModel,EmailStr, constr
from typing import Annotated

class BaseUsers(BaseModel):
    user_id: str
    userEmail: EmailStr
    userFullName: str
    user_pwd: Annotated[str, constr(min_length=8, max_length=64)]