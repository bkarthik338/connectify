import json
import os
from datetime import datetime
from datetime import timedelta

from utility.user_utility import generate_jwt_token


def create_payload_jwt(user_id: str, exp_time: bool) -> dict:
    if exp_time:
        exp_time = datetime.utcnow() - timedelta(minutes=30)
    else:
        exp_time = datetime.utcnow() + timedelta(days=1)
    return {"user_id": user_id, "exp": exp_time}


def generate_jwt_token_test(user_id: str, exp_time: bool = False) -> str:
    payload = create_payload_jwt(user_id=user_id, exp_time=exp_time)
    return generate_jwt_token(payload)


base_url = os.environ.get("BASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
tweet_json_file_path = os.path.join(
    current_dir, "../testdata/tweet_testcases.json"
)

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


def load_tweet_json_file():
    """
    This function is to load tweet test data json file
    """
    with open(tweet_json_file_path) as file:
        data = json.load(file)
    return data
