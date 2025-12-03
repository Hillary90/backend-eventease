from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str
