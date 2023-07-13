import json
import os

from dotenv import load_dotenv

from models.user_model import GeneralResponse
from mutation.tweet_mutation import TweetMutation


tweetMutationInstance = TweetMutation()


load_dotenv()
Info = None
base_url = os.environ.get("BASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
tweet_json_file_path = os.path.join(
    current_dir, "../testdata/tweet_testcases.json"
)


def load_tweet_json_file():
    """
    This function is to load tweet test data json file
    """
    with open(tweet_json_file_path) as file:
        data = json.load(file)
    return data


def create_post_test(testcase: str, token: str) -> GeneralResponse:
    """
    This function is to check CreatePost API
    """
    data = load_tweet_json_file()[testcase]
    response = tweetMutationInstance.create_tweet(
        Info,
        token=token,
        description=data["description"],
        # hashtags=data["hashtags"]
    )
    return response
