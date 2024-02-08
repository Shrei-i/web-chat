from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool = True


    