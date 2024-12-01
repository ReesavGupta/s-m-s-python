from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI") 

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.student

students_collection = database.get_collection("students")

try:
  print(f'Database: {client.list_database_names()}')
except Exception as e:
  print(f'There was an error while conencting to the db: {e}')


