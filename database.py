# datatbase connection file
from pymongo import MongoClient


# Load environment variables from .env file
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["test-connectify-db"]
