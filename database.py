# datatbase connection file
import os

from dotenv import load_dotenv
from pymongo import MongoClient


# Load environment variables from .env file
load_dotenv()
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["test-connectify-db"]
