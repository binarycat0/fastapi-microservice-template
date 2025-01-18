from pydantic import BaseModel


class UserBaseModel(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreateModel(UserBaseModel):
    pass


class UserResponseModel(UserBaseModel):
    id: int

    class Config:
        from_attributes = True
