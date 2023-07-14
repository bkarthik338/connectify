import json
import os
from datetime import datetime
from datetime import timedelta
from typing import Any

from dotenv import load_dotenv

from models.user_model import GeneralResponse
from models.user_model import GetUserResponse
from models.user_model import LoginResponse
from models.user_model import UpdateUserInput
from mutation.user_mutation import UserMutation
from query.user_query import UserQuery
from utility.user_utility import generate_jwt_token


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


def create_payload_jwt(user_id: str, exp_time: bool) -> dict:
    if exp_time:
        exp_time = datetime.utcnow() - timedelta(minutes=30)
    else:
        exp_time = datetime.utcnow() + timedelta(days=1)
    return {"user_id": user_id, "exp": exp_time}


def generate_jwt_token_test(user_id: str, exp_time: bool = False) -> str:
    payload = create_payload_jwt(user_id=user_id, exp_time=exp_time)
    return generate_jwt_token(payload)


def create_test_user(testcase: str) -> GeneralResponse:
    """
    This function is to create test user.
    Parameters are passed for negative test cases
    :Invalid Username/Email
    """
    data = load_user_json_file()[testcase]
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


def delete_test_user(testcase: str) -> GeneralResponse:
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


def update_test_user(testcase: str, token: str) -> GeneralResponse:
    """
    This fuction is to check Update User API
    """
    data = load_user_json_file()[testcase]
    response = userMutationInstance.update_user(
        Info,
        token=token,
        user_input=UpdateUserInput.from_json(json.dumps(data)),
    )
    return response


def reset_password_test_user(testcase: str, token: str) -> GeneralResponse:
    """
    This function is to check Reset Password API
    """
    data = load_user_json_file()[testcase]
    response = userMutationInstance.reset_password(
        Info,
        token=token,
        oldPassword=data["old_password"],
        newPassword=data["new_password"],
    )
    return response
