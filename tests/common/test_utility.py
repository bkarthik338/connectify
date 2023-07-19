import json
import os
from datetime import datetime
from datetime import timedelta

from models.user_model import GeneralResponse
from models.user_model import LoginResponse
from mutation.user_mutation import UserMutation
from query.user_query import UserQuery
from utility.user_utility import generate_jwt_token

Info = None

userMutationInstance = UserMutation()
userQueryInstance = UserQuery()

base_url = os.environ.get("BASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
tweet_json_file_path = os.path.join(
    current_dir, "../testdata/tweet_testcases.json"
)

user_json_file_path = os.path.join(
    current_dir, "../testdata/user_testcases.json"
)

like_json_file_path = os.path.join(
    current_dir, "../testdata/like_testcases.json"
)


def load_json_file(filepath: str):
    """
    This function is to load tweet test data json file
    """
    with open(filepath) as file:
        data = json.load(file)
    return data


userTestDataJson = load_json_file(user_json_file_path)
tweetTestDataJson = load_json_file(tweet_json_file_path)
likeTestDataJson = load_json_file(like_json_file_path)


def create_users(users_list=[]) -> dict:
    # Create Test User For Testing
    loggedinusertokendict = {}
    for user in users_list:
        data = userTestDataJson[user]
        response = userMutationInstance.create_user(
            Info,
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )
        assert isinstance(response, GeneralResponse)
        assert (
            response.success
        ), "Creating Test User Failed In The Setup Function"
        assert response.msg.startswith("User created Successfully")

        # Login And Get The Token
        data = userTestDataJson[user]
        response = userQueryInstance.userlogin(
            Info,
            username=data["username"],
            password=data["password"],
            exp_time=None,
        )
        assert isinstance(response, LoginResponse)
        assert (
            response.success
        ), "Unable To Capture Token For Tweet Module Testing"
        assert response.msg.startswith("Login Successful")
        loggedinusertokendict[user] = response.token
    return loggedinusertokendict


def delete_users(users_list=[]) -> str:
    # Delete Test Users
    for user in users_list:
        data = userTestDataJson[user]
        response = userMutationInstance.delete_user(
            Info, username=data["username"]
        )
        assert isinstance(response, GeneralResponse)
        assert response.success, "Unable To Delete Created Test User"
        assert response.msg == "User is deleted."
    return "Users Deleted"


def create_payload_jwt(user_id: str, exp_time: bool) -> dict:
    if exp_time:
        exp_time = datetime.utcnow() - timedelta(minutes=30)
    else:
        exp_time = datetime.utcnow() + timedelta(days=1)
    return {"user_id": user_id, "exp": exp_time}


def generate_jwt_token_test(user_id: str, exp_time: bool = False) -> str:
    payload = create_payload_jwt(user_id=user_id, exp_time=exp_time)
    return generate_jwt_token(payload)
