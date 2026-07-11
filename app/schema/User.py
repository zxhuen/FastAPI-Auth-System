from pydantic import BaseModel, EmailStr, ConfigDict, Field 
from uuid import UUID


class RoleResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr
    hashed_password: str = Field(
        min_length=8,
        max_length=128
    )

class UserResponse(BaseModel):
    id: UUID
    role: RoleResponse
    username: str
    email: EmailStr


    class Config:
        from_attributes = True

class EditUser(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr

class user_login(BaseModel):
    username: str
    password: str




class current_user(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: RoleResponse

    class Config:
        from_attributes = True


class searchResponse(BaseModel):
    username: str

    class Config:
        from_attributes = True

class reset_password(BaseModel):
    password: str = Field(
        min_length=8,
        max_length=128
    )


