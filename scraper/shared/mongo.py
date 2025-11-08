import os
import ssl
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# IF YOU ARE HAVING ISSUES CONNECTING TO MONGO DB, MAKE SURE IP ADDRESS IS ADDED
# https://cloud.mongodb.com/v2/690f7ebe9b586528bc78f832#/security/network/accessList

def get_mongo_client():
    """
    Initialize and return a MongoDB client using environment variables.
    """
    connection_string = os.getenv('MONGO_CONNECTION_STRING')
    if not connection_string:
        raise ValueError("MONGO_CONNECTION_STRING environment variable is not set")

    return MongoClient(connection_string)

def get_database(client):
    """
    Get a database from the MongoDB client.
    """
    return client["housing"]["postings"]
