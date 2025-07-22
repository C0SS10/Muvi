from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME")

mongodb_client = MongoClient(MONGODB_URI)
database: Database = mongodb_client.get_database(DATABASE_NAME)