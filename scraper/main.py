from shared.mongo import get_mongo_client, get_database


if __name__ == "__main__":
    client = get_mongo_client()
    print("Connected to MongoDB")
    
    # Get the postings collection from housing database
    collection = get_database(client)
    
    # Read all documents from the postings collection
    documents = list(collection.find())
    print(f"Found {len(documents)} documents in postings collection:")
    for doc in documents:
        print(doc)
    
