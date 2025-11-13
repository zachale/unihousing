import requests
from bs4 import BeautifulSoup as bs4

from shared.mongo import delete_id, get_database, get_mongo_client

# Constants
API_URL = "https://thecannon.ca"
HEADERS = {
    "Content-Type": "text/html",
    "Accept": "text/html",
}


def get_mongo_db_ids() -> dict[str, str]:
    """
    Fetch all listing IDs from the MongoDB database.
    Returns a dictionary mapping listing IDs to their MongoDB `_id`.
    """
    client = get_mongo_client()
    collection = get_database(client)
    try:
        # Get all entries and extract the field `_id`
        cur = collection.find({}, {"_id": 1, "listing_id": 1})
        ids = {}

        for doc in cur:
            _id = doc.get("_id")
            listing_id = doc.get("listing_id")
            if _id is not None and listing_id is not None:
                ids[listing_id] = _id
        return ids
    finally:
        client.close()


def get_housing_info() -> dict[str, str]:
    page = 1
    housing_links = {}

    while True:
        print(f"Fetching page: {page}")
        response = requests.get(f"{API_URL}/housing/page/{page}", headers=HEADERS)
        if not response.ok:
            print(f"Error: Unable to fetch the housing page on page {page}")
            return housing_links

        html = bs4(response.text, "html.parser")
        links = html.select(f'a[href^="{API_URL}/classified/housing"]')

        # If no housing links are found, break the loop!
        if not links:
            break

        for link in links:
            print(f"Found housing link: {link['href']}")
            posting_response = requests.get(link["href"], headers=HEADERS)
            if not posting_response.ok:
                print(f"Error: Unable to fetch the posting at {link['href']}")
                continue

            posting_html = bs4(posting_response.text, "html.parser").prettify()
            housing_links[link["href"]] = posting_html

        requests.get(f"{API_URL}/classified/housing/page/{page}")
        page += 1

    return housing_links


def main():
    housing_info = get_housing_info()
    if not housing_info:
        print("No housing information found")
        return

    existing_ids = get_mongo_db_ids()
    print(f"Existing IDs in database: {existing_ids}")

    for url, _ in housing_info.items():
        listing_id = url.rstrip(" /").split("/")[-1]
        if listing_id in existing_ids:
            # Listing exists, remove it from existing_ids to avoid deletion
            del existing_ids[listing_id]

    # The leftover IDs should be deleted from the database (delete)
    print(f"Deleting listings with IDs: {existing_ids.values()}")
    deleted_count = delete_id(list(existing_ids.values()))
    print(f"Deleted {deleted_count} listings from the database")

    # Process ALL listings (create, update, etc.)
    for url, _ in housing_info.items():
        listing_id = url.rstrip(" /").split("/")[-1]
        print(f"Processing listing with ID: {listing_id}")
        # TODO: Send this data to a queue


if __name__ == "__main__":
    main()
