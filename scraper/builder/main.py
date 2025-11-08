
"""Entry points for parsing housing listings from HTML payloads."""

from __future__ import annotations

import json
from typing import Any

from .parse_listings import parse_listing_html
from .description_extractor import extract_description


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

    extracted_fields = extract_description(parsed_listing['description'])
    if isinstance(extracted_fields, dict):
        parsed_listing.update(extracted_fields)
        
    return {
        "statusCode": 200,
        "body": json.dumps(parsed_listing, ensure_ascii=False),
    }

