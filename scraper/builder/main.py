
"""Entry points for parsing housing listings from HTML payloads."""

from __future__ import annotations

import json
from typing import Any, Iterable
from .parse_listings import parse_listing_html

def _parse_many(html_payloads: Iterable[tuple[str | None, str]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for listing_id, html in html_payloads:
        parsed = parse_listing_html(html)
        if listing_id:
            parsed.setdefault("listing_id", listing_id)
        results.append(parsed)
    return results


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

    to_parse = [(listing_id, html_content)]

    try:
        parsed_results = _parse_many(to_parse)
    except Exception as exc:  # pragma: no cover - defensive catch for robustness
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to parse HTML: {exc}"}),
        }

    body_payload: Any = parsed_results
    if len(parsed_results) == 1:
        body_payload = parsed_results[0]

    return {
        "statusCode": 200,
        "body": json.dumps(body_payload, ensure_ascii=False),
    }

