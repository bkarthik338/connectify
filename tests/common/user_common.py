import json
import os
from typing import Any

from dotenv import load_dotenv

from models.user_model import CreateUserResponse
from models.user_model import DeleteUserResponse
from models.user_model import GetUserResponse
from models.user_model import LoginResponse
from mutation.user_mutation import UserMutation
from query.user_query import UserQuery


# Load environment variables from .env file
load_dotenv()
Info = None
base_url = os.environ.get("BASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
user_json_file_path = os.path.join(
    current_dir, "../testdata/user_testcases.json"
)


# Instances for Query and Mutation Classes
userMutationInstance = UserMutation()
userQueryInstance = UserQuery()


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
    print("Inside Create test user")
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    return response


def get_test_user(token: str) -> GetUserResponse:
    """
    This function is to get test user
    """
    response = userQueryInstance.getuser(Info, token)
    return response


def delete_test_user(testcase: str) -> DeleteUserResponse:
    """
    This function is to delete created test user and testing
    the api as well
    """
    data = load_user_json_file()[testcase]
    response = userMutationInstance.delete_user(
        Info, username=data["username"]
    )
    return response


def login_test_user(testcase: str, exp_time: Any = None) -> LoginResponse:
    """
    This function is to check the login API
    """
    data = load_user_json_file()[testcase]
    response = userQueryInstance.userlogin(
        Info,
        username=data["username"],
        password=data["password"],
        exp_time=exp_time,
    )
    return response
