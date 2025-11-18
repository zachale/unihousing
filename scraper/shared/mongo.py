import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import List, Dict, Any, Tuple

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


def delete_id(id: list[str | ObjectId]) -> int:
    """
    Takes a list of listing IDs and deletes them from the database.

    Parameters:
    - id: List of listing IDs (as strings or ObjectIds)

    Returns:
    - int: Number of IDs deleted
    """
    client = get_mongo_client()
    collection = get_database(client)

    try:
        # Convert all IDs to ObjectId instances
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

        # Delete listings with the given IDs
        filter_query = {"_id": {"$in": object_ids}}

        # Delete the listings
        result = collection.delete_many(filter_query)

        return result.deleted_count
    finally:
        client.close()

def get_listings(page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
    """
    Return paginated listings sorted by recency (recently posted) 

    Parameters: 
    - page: Page number (default is 1)
    - page_size: Number of listings per page 

    Returns: 
    - (items, total count)
    """
    client = get_mongo_client()
    collection = get_database(client) # gets values from the "postings" collection 

    try: 
        skip = (page - 1) * page_size

        # sort by date posted 
        cursor = (
            collection.find()
            .sort("date_posted", -1)  # Sort by date_posted in descending order
            .skip(skip)
            .limit(page_size)
        )
        items: List[Dict[str, Any]] = []

        for doc in cursor: 
            # convert the _id to a string field called "id"
            doc["id"] = str(doc["_id"])
            doc.pop("_id", None)  # remove the original _id field

            items.append(doc)

        total = collection.count_documents({})

        return items, total
    finally:
        client.close()


    
