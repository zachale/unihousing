
"""Entry points for parsing housing listings from HTML payloads."""

from __future__ import annotations

import json
from typing import Any

from scraper.shared.mongo import get_mongo_client, get_database
from .parse_listings import parse_listing_html
from .checksum import json_checksum, string_checksum

def handler(event: dict[str, Any], context: Any | None = None) -> dict[str, Any]:
    html_content = event.get("html_content")
    listing_id = event.get("listing_id")

    if html_content is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No HTML content provided."}),
        }

    if not isinstance(html_content, str):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "html_content must be a string."}),
        }

    try:
        parsed_listing = parse_listing_html(html_content)
    except Exception as exc:  # pragma: no cover - defensive catch for robustness
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to parse HTML: {exc}"}),
        }
    if listing_id:
        parsed_listing.setdefault("listing_id", listing_id)
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(parsed_listing, ensure_ascii=False),
        }

    client = get_mongo_client()
    collection = get_database(client)
    existing_listing = collection.find_one({"_id": listing_id})

    new_json_checksum = json_checksum(parsed_listing)
    new_desc_checksum = string_checksum(parsed_listing.get("description", ""))

    updates: dict[str, Any] = {}

    if existing_listing:
        if new_json_checksum != existing_listing.get("check_sum_json"):
            updates["check_sum_json"] = new_json_checksum

        if new_desc_checksum != existing_listing.get("check_sum_description"):
            # TODO: trigger downstream enrichment when description changes
            updates["check_sum_description"] = new_desc_checksum

        if updates:
            updates.update(parsed_listing)
            collection.update_one({"_id": listing_id}, {"$set": updates})
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No changes detected."}),
            }
    else:
        parsed_listing.update(
            {
                "_id": listing_id,
                "check_sum_json": new_json_checksum,
                "check_sum_description": new_desc_checksum,
            }
        )
        collection.insert_one(parsed_listing)

    return {
        "statusCode": 200,
        "body": json.dumps(parsed_listing, ensure_ascii=False),
    }

