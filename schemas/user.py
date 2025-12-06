from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str   

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    email: EmailStr

