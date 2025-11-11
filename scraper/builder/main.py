"""Entry points for parsing housing listings from HTML payloads."""

from __future__ import annotations

import json
from typing import Any

from shared.mongo import get_database, get_mongo_client

from .checksum import json_checksum, string_checksum
from .description_extractor import extract_description
from .parse_listings import parse_listing_html


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
    has_existing_listing = existing_listing is not None
    existing_listing = existing_listing or {}

    db_listing = dict(parsed_listing)
    description_text = parsed_listing.get("description") or ""

    new_json_checksum = json_checksum(db_listing)
    new_desc_checksum = string_checksum(description_text)

    if not has_existing_listing:
        extracted_fields = extract_description(description_text) if description_text else {}
        if extracted_fields:
            db_listing.update(extracted_fields)
        document = {
            "_id": listing_id,
            **db_listing,
            "check_sum_json": new_json_checksum,
            "check_sum_description": new_desc_checksum,
        }
        collection.insert_one(document)
    else:
        updates: dict[str, Any] = {}
        if new_json_checksum != existing_listing.get("check_sum_json"):
            updates["check_sum_json"] = new_json_checksum
            updates.update(db_listing)

        if new_desc_checksum != existing_listing.get("check_sum_description"):
            extracted_fields = extract_description(description_text) if description_text else {}
            if extracted_fields:
                db_listing.update(extracted_fields)
            updates["check_sum_description"] = new_desc_checksum
            updates.update(db_listing)

        if updates:
            collection.update_one({"_id": listing_id}, {"$set": updates})

    return {
        "statusCode": 200,
        "body": json.dumps(parsed_listing, ensure_ascii=False),
    }
