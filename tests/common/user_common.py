import json
import os

from dotenv import load_dotenv

from mutation.user_mutation import CreateUserResponse
from mutation.user_mutation import DeleteUserResponse
from mutation.user_mutation import UserMutation
from query.user_query import GetUserResponse
from query.user_query import UserQuery


# Load environment variables from .env file
load_dotenv()
Info = None
base_url = os.environ.get("BASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
user_json_file_path = os.path.join(
    current_dir, "../testdata/user_testcases.json"
)


def load_user_json_file():
    """
    This function is to load use test data json file
    """
    with open(user_json_file_path) as file:
        data = json.load(file)
    return data


def create_test_user(testcase: str) -> CreateUserResponse:
    """
    This function is to create test user.
    Parameters are passed for negative test cases
    :Invalid Username/Email
    """
    data = load_user_json_file()[testcase]
    userMutationInstance = UserMutation()
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    return response


def get_test_user() -> GetUserResponse:
    """
    This function is to get test user
    """
    data = load_user_json_file()["getTestUser"]
    userQueryInstance = UserQuery()
    response = userQueryInstance.getuser(Info, username=data["username"])
    return response


def delete_test_user(testcase: str) -> DeleteUserResponse:
    """
    This function is to delete created test user and testing
    the api as well
    """
    data = load_user_json_file()[testcase]
    userMutationInstance = UserMutation()
    response = userMutationInstance.delete_user(
        Info, username=data["username"]
    )
    return response
