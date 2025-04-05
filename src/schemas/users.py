from pydantic import BaseModel, ConfigDict


class UserBaseModel(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreateModel(UserBaseModel):
    pass


class UserResponseModel(UserBaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
