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
