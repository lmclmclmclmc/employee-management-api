from pydantic import BaseModel, ConfigDict, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    department: str = Field(
        default="General",
        min_length=1,
        max_length=100,
    )
    salary: float = Field(ge=0)


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    department: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    salary: float | None = Field(default=None, ge=0)


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    department: str
    salary: float
