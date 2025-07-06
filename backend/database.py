import os
from pymongo import MongoClient
from dotenv import load_dotenv

# environment variables for connection
load_dotenv()

# get MongoDB URI from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/Myrecipesaver")

try:
    client = MongoClient(MONGO_URI)
    db = client.get_database() 

    # references to the collections
    users_collection = db.users
    recipes_collection = db.recipes

    print(f"Successfully connected to MongoDB database: {db.name}")

except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)

# You can define functions to access these collections in other parts of your app
def get_users_collection():
    return users_collection

def get_recipes_collection():
    return recipes_collection