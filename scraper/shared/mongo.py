import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# IF YOU ARE HAVING ISSUES CONNECTING TO MONGO DB, MAKE SURE IP ADDRESS IS ADDED
# https://cloud.mongodb.com/v2/690f7ebe9b586528bc78f832#/security/network/accessList


def get_mongo_client():
    """
    Initialize and return a MongoDB client using environment variables.
    """
    connection_string = os.getenv("MONGO_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGO_CONNECTION_STRING environment variable is not set")

    return MongoClient(connection_string)


def get_database(client):
    """
    Get a database from the MongoDB client.
    """
    return client["housing"]["postings"]


def get_listing_by_id(collection, listing_id):
    """
    Fetch a listing from the database by its listing_id.

    Parameters:
    - listing_id: The listing ID to search for (as a string or ObjectId)

    Returns:
    - dict | None: The listing document if found, otherwise None
    """
    client = get_mongo_client()
    collection = get_database(client)

    # Convert string ID to ObjectId if necessary
    if isinstance(listing_id, str):
        try:
            listing_id = ObjectId(listing_id)
        except Exception:
            return None

    return collection.find_one({"_id": listing_id})


def archive_id(id):
    """
    Takes a list of listing IDs and archives them by setting archived from false to true.

    Parameters:
    - id: List of listing IDs (as strings or ObjectIds)

    Returns:
    - int: Number of IDs archived
    """
    client = get_mongo_client()
    collection = get_database(client)

    # Convert string IDs to ObjectIds
    object_ids = []
    for id_str in id:
        try:
            if isinstance(id_str, str):
                object_ids.append(ObjectId(id_str))
            elif isinstance(id_str, ObjectId):
                object_ids.append(id_str)
            else:
                continue
        except Exception:
            continue

    if not object_ids:
        return 0

    # Find listings with the given IDs where archived = false
    filter_query = {"_id": {"$in": object_ids}, "archived": False}

    # Set archived = true
    update_query = {"$set": {"archived": True}}

    # Update the listings
    result = collection.update_many(filter_query, update_query)

    return result.modified_count
