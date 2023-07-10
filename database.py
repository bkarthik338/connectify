import os

from dotenv import load_dotenv
from pymongo import MongoClient


# Load environment variables from .env file
load_dotenv()
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
client = MongoClient(f"mongodb://{db_host}:{db_port}/")
db = client[db_name]
