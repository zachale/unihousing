import argparse
import re
from urllib.parse import urlparse
from pathlib import Path
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import sys


def fetch_and_save(id_segment: str, output_dir: Path, save_plain_text: bool = False) -> bool:
    """Fetch the page for id_segment and save output to output_dir/<id_segment>.txt.

    Returns True on success, False on failure.
    """
    url = f"https://thecannon.ca/classified/housing/{id_segment}/"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except RequestException as exc:
        print(f"[ERROR] Failed to fetch {url}: {exc}")
        return False

    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    if save_plain_text:
        content = soup.get_text(separator="\n", strip=True)
    else:
        content = soup.prettify()

    output_path = output_dir / f"{id_segment}.txt"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as exc:
        print(f"[ERROR] Failed to write {output_path}: {exc}")
        return False

    print(f"Saved cleaned output to: {output_path}")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch classifieds by numeric id and save cleaned output to html/<id>.txt"
    )
    parser.add_argument("ids", nargs="+", help="One or more numeric id segments from the URL")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Save plain text (stripped of HTML tags) instead of prettified HTML",
    )
    args = parser.parse_args(argv)

    ids = args.ids
    # Validate ids
    valid_ids: list[str] = []
    invalid_ids: list[str] = []
    for _id in ids:
        if re.fullmatch(r"\d+", _id):
            valid_ids.append(_id)
        else:
            invalid_ids.append(_id)

    if invalid_ids:
        print(f"[WARN] Skipping invalid (non-numeric) ids: {', '.join(invalid_ids)}")

    if not valid_ids:
        print("No valid numeric ids provided. Exiting.")
        return 2

    output_dir = Path(__file__).resolve().parent / "html"
    output_dir.mkdir(parents=True, exist_ok=True)

    successes = 0
    failures = 0
    for id_segment in valid_ids:
        print(f"Processing id: {id_segment} ...")
        ok = fetch_and_save(id_segment, output_dir, save_plain_text=args.text)
        if ok:
            successes += 1
        else:
            failures += 1

    print(f"Done. Successes: {successes}, Failures: {failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())