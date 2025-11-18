import os
import sys
from pathlib import Path
from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import DESCENDING 

# Make project root importable so we can reach scraper/shared/mongo.py
BASE_DIR = Path(__file__).resolve().parent.parent  # /.../unihousing
sys.path.append(str(BASE_DIR))

from scraper.shared.models import Listing
from scraper.shared.mongo import ( 
    get_mongo_client,
    get_database,
    get_listings as mongo_get_listings,
)

app = FastAPI(title="UniHousing API")


# ---------- Pydantic models ----------


class PaginatedListings(BaseModel):
    page: int
    limit: int
    total: int
    items: List[Listing]


@app.get("/api/listings", response_model=PaginatedListings)
def get_listings(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    """
    Use scraper.shared.mongo.get_listings() to fetch paginated data.
    That function already handles:
      - creating the client
      - querying Mongo
      - closing the client
      - returning (items, total)
    """
    items_raw, total = mongo_get_listings(page=page, page_size=limit)
    items = [Listing(**doc) for doc in items_raw]

    return PaginatedListings(
        page=page,
        limit=limit,
        total=total,
        items=items,
    )

@app.get("/api/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: str):
    """
    Get a single listing by its `listing_id` field.

    Uses shared.mongo.get_mongo_client() and get_database() which returns
    the `housing.postings` MongoDB collection.
    """
    client = get_mongo_client()
    postings = get_database(client)  # clearer name

    try:
        doc = postings.find_one({"listing_id": listing_id})
        if not doc:
            raise HTTPException(status_code=404, detail="Listing not found")

        # Convert MongoDB _id → id (string)
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)

        return Listing(**doc)
    finally:
        client.close()