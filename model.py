# File represents the table columns/type
import strawberry


# User Model
@strawberry.type
class User:
    id: str
    username: str
    email: str
    password: str = None
