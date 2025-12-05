from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    name: str
    email: str
    password: Optional[str] = None
    password: Optional[str] = None  

