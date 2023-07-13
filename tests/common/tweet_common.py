import json
import os
from typing import Union

from dotenv import load_dotenv

from models.tweet_model import ListTweetModel
from models.user_model import GeneralResponse
from mutation.tweet_mutation import TweetMutation
from query.tweet_query import TweetQuery


tweetMutationInstance = TweetMutation()
tweetQueryInstance = TweetQuery()


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


def get_all_tweets(token: str) -> Union[GeneralResponse, ListTweetModel]:
    """
    This function is to check getAllTweets API
    """
    response = tweetQueryInstance.my_tweets(Info, token=token)
    return response
