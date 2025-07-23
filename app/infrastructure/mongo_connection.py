from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

env = os.getenv("ENVIRONMENT", "local")

if env == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env.local")

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME")

mongodb_client = MongoClient(MONGODB_URI)
database: Database = mongodb_client.get_database(DATABASE_NAME)