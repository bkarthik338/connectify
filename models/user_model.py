import dataclasses
import json
from typing import Optional

import strawberry


# User Model
@strawberry.type
class User:
    id: str
    username: str
    email: str
    password: str = None


# SignUP API Response
@strawberry.type
class CreateUserResponse:
    success: bool
    msg: str


# Delete User API Response
@strawberry.type
class DeleteUserResponse:
    success: bool
    msg: str


# Getting User API Response
@strawberry.type
class GetUserResponse:
    data: User
    success: bool


# Getting User API Failure Response
# (Invalid Request/Parameter)
@strawberry.type
class GetUserFailureResponse:
    error: str
    success: bool


# LoginAPI Success/Failure Response
@strawberry.type
class LoginResponse:
    msg: str
    success: bool
    token: str = None


# User Update API
@strawberry.type
class UpdateUserResponse:
    msg: str
    success: bool


# Update User Input
@strawberry.input
class UpdateUserInput:
    email: Optional[str] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, json_data: str) -> "UpdateUserInput":
        data = json.loads(json_data)
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
