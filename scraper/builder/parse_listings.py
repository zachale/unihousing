

from __future__ import annotations

from typing import Any

from bs4 import BeautifulSoup

from .constants import FIELD_ALIASES



def text_or_none(node) -> str | None:
    """Return the trimmed text for ``node`` or ``None`` if the node is missing."""

    if node is None:
        return None
    return node.get_text(" ", strip=True)


def parse_listing_html(html: str) -> dict[str, Any]:
    """Parse a single listing HTML document and return the extracted fields."""

    soup = BeautifulSoup(html, "html.parser")

    details_root = soup.select_one("dl.classified-details.housing")
    if details_root is None:
        raise ValueError("Could not find listing details block (dl.classified-details.housing)")

    # Headline is the h1 right before the details block.
    headline = text_or_none(details_root.find_previous("h1"))

    primary_row = details_root.select_one(".row.space-between")
    address = None
    price = None
    if primary_row is not None:
        address = text_or_none(primary_row.select_one(".md"))
        price = text_or_none(primary_row.select_one("strong"))

    description = text_or_none(details_root.find("dd", class_="description"))

    # Build a lookup of DT/DD pairs in the metadata rows.
    metadata: dict[str, str | None] = {}
    for row in details_root.select(".well .row"):
        for column in row.find_all("div", recursive=False):
            label = column.find("dt")
            value = column.find("dd")
            if not label or not value:
                continue
            metadata[label.get_text(strip=True)] = text_or_none(value)

    photos: list[str] = []
    seen: set[str] = set()
    for anchor in details_root.select("#photos a[href]"):
        href = anchor.get("href")
        if not href:
            continue
        href = href.strip()
        if not href or href in seen:
            continue
        seen.add(href)
        photos.append(href)

    if not photos:
        for image in details_root.select("#photos img[src]"):
            src = image.get("src")
            if not src:
                continue
            src = src.strip()
            if not src or src in seen:
                continue
            seen.add(src)
            photos.append(src)

    feature_texts: set[str] = set()
    for item in details_root.select(".housing-features li"):
        tooltip = item.select_one(".tooltip")
        if tooltip:
            text = tooltip.get_text(strip=True)
            if text:
                feature_texts.add(text.casefold())
        image = item.find("img")
        if image:
            alt_text = image.get("alt")
            if alt_text:
                feature_texts.add(alt_text.strip().casefold())

    feature_fields = {
        "parking",
        "no_smoking",
        "laundry_facilities",
        "cooking_facilities",
    }

    extracted: dict[str, Any] = {
        "headline": headline,
        "address": address,
        "price": price,
        "description": description,
        "photos": photos,
    }

    for field in feature_fields:
        label = FIELD_ALIASES[field]
        extracted[field] = label.casefold() in feature_texts

    for field, label in FIELD_ALIASES.items():
        if field in feature_fields:
            continue
        value = metadata.get(label)
        if value is None:
            continue
        extracted[field] = value

    return extracted